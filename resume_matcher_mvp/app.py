import gradio as gr
import re
from datetime import datetime
from typing import Tuple, List, Dict

# Import custom modules
from src.embeddings import EmbeddingEngine
from src.domain_classifier import DomainClassifier
from src.text_profile_parser import TextProfileParser
from src.role_mapper import RoleMapper
from sample_data.sample_jds import get_sample_jd, get_all_roles


class ResumeMatcherApp:
    """App refactored for direct JD vs Profile vector similarity.

    This version removes resume uploads and vector DB search. It accepts a Job
    Description and a Candidate Profile text and computes the cosine similarity
    between their sentence-transformer embeddings. It also runs a simple domain
    classifier and parses the profile sections for additional context.
    """

    def __init__(self):
        print("Initializing JD vs Profile Matching Application...")
        self.embedding_engine = EmbeddingEngine()
        self.domain_classifier = DomainClassifier()
        self.text_profile_parser = TextProfileParser()
        print("Application initialized successfully!")

    # --------------------------
    # Helpers
    # --------------------------
    def _strip_trailing_list(self, text: str) -> str:
        """Remove a trailing bracketed list (like an array of questions) if present.

        The input sometimes contains a resume-like text followed by a JSON-like
        array (e.g., interview questions). We remove that to focus similarity on
        the profile content only.
        """
        if not text:
            return ""
        lines = text.splitlines()
        kept: List[str] = []
        in_block = False
        for ln in lines:
            s = ln.strip()
            if not in_block and s.startswith("["):
                in_block = True
                # do not keep this line
                continue
            if in_block:
                if s.endswith("]"):
                    in_block = False
                # skip lines inside the bracketed list
                continue
            kept.append(ln)
        cleaned = "\n".join(kept).strip()
        return cleaned if cleaned else text.strip()

    def _basic_clean(self, text: str) -> str:
        # Remove excessive asterisks and normalize whitespace
        t = re.sub(r"\*{2,}", " ", text or "")
        t = re.sub(r"\s+", " ", t)
        return t.strip()

    # --------------------------
    # Core logic
    # --------------------------
    def match_profile_to_jd(self, job_description: str, profile_text: str) -> Tuple[float, str]:
        """Compute similarity between JD and Profile text and return score and details.

        Returns:
          - similarity score in [0,1]
          - details string with domain hints, overlapping keywords and parsed stats
        """
        jd = (job_description or "").strip()
        raw_profile = (profile_text or "").strip()
        if not jd:
            return 0.0, "Please enter a job description."
        if not raw_profile:
            return 0.0, "Please paste the candidate profile text."

        # Preprocess profile: drop trailing Q/A or question list sections
        prof_main = self._strip_trailing_list(raw_profile)
        jd_clean = self._basic_clean(jd)
        prof_clean = self._basic_clean(prof_main)

        # Generate embeddings and compute similarity
        try:
            jd_emb = self.embedding_engine.generate_embedding(jd_clean)
            prof_emb = self.embedding_engine.generate_embedding(prof_clean)
            sim = self.embedding_engine.calculate_similarity(jd_emb, prof_emb)
        except Exception as e:
            return 0.0, f"Embedding error: {str(e)}"

        # Domains
        jd_domain, jd_conf, jd_tokens = self.domain_classifier.classify(jd_clean)
        pf_domain, pf_conf, pf_tokens = self.domain_classifier.classify(prof_clean)

        # Overlapping domain-related tokens
        overlap = []
        try:
            overlap = sorted(list(set(jd_tokens).intersection(set(pf_tokens))))
        except Exception:
            overlap = []

        # Parse profile for section stats
        parsed = self.text_profile_parser.parse(prof_main)
        edu_n = len(parsed.get("education", []))
        ach_n = len(parsed.get("achievements", []))
        proj_n = len(parsed.get("projects", []))
        exp_n = len(parsed.get("experience", []))
        cert_n = len(parsed.get("certificates", []))

        details_lines = [
            f"Similarity: {sim:.2%}",
            f"JD domain: {jd_domain} (conf {jd_conf:.2f})",
            f"Profile domain: {pf_domain} (conf {pf_conf:.2f})",
        ]
        if overlap:
            details_lines.append(f"Overlapping domain keywords: {', '.join(overlap[:12])}")
        details_lines.append(
            f"Profile sections parsed -> education: {edu_n}, achievements: {ach_n}, projects: {proj_n}, experience: {exp_n}, certificates: {cert_n}"
        )

        return float(sim), "\n".join(details_lines)


def create_interface():
    """Create and configure Gradio interface for JD vs Profile matching."""
    app = ResumeMatcherApp()

    with gr.Blocks(title="JD ↔ Profile Matching", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🔎 JD ↔ Candidate Profile Semantic Match")
        gr.Markdown(
            "**Both inputs support the same structured format** with sections like **Education**, **Projects**, **Work Experience**, etc. The app computes cosine similarity between their embeddings and provides domain analysis."
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## 📋 Job Description / Requirements")
                with gr.Row():
                    sample_role = gr.Dropdown(
                        choices=get_all_roles(),
                        label="Load Sample JD",
                        value="Software Engineer",
                    )
                    load_sample_btn = gr.Button("Load Sample")

                job_description = gr.Textbox(
                    label="Job Description or Requirements",
                    placeholder="Paste job description or requirements in structured format:\n\n**Requirements**\n- 3+ years Python experience\n- Machine learning background\n\n**Responsibilities**\n- Build ML models\n- Collaborate with teams\n\n(Or use traditional JD format)",
                    lines=15,
                    max_lines=25,
                )

            with gr.Column(scale=1):
                gr.Markdown("## 👤 Candidate Profile")
                profile_text = gr.Textbox(
                    label="Candidate Profile Text",
                    placeholder="Paste candidate profile in structured format:\n\n**Education**\npostgraduate - University Name - CGPA\n\n**Projects**\nProject Name - Description with technologies used\n\n**Work experience and internships**\nfull time - Company - dates - Description\n\n**Achievements**\nachievement - type - Description\n\n(Trailing question lists will be automatically ignored)",
                    lines=20,
                    max_lines=30,
                )

        compute_btn = gr.Button("Compute Fit", variant="primary")

        with gr.Row():
            fit_score = gr.Number(label="Fit Score (0–1)", interactive=False)
            details = gr.Textbox(label="Details", lines=10, max_lines=18, interactive=False)

        # Events
        load_sample_btn.click(
            fn=get_sample_jd,
            inputs=[sample_role],
            outputs=[job_description],
        )

        compute_btn.click(
            fn=app.match_profile_to_jd,
            inputs=[job_description, profile_text],
            outputs=[fit_score, details],
        )

        with gr.Accordion("Usage Notes", open=False):
            gr.Markdown(
                """
                - Fit score is cosine similarity of embeddings; values closer to 1 indicate stronger semantic alignment.
                - The parser attempts to extract sections like education, achievements, projects, experience, and certificates from the profile text.
                - If the profile text includes a trailing list (e.g., interview questions), it is ignored for similarity.
                """
            )

    return interface


if __name__ == "__main__":
    ui = create_interface()
    ui.launch(
        share=True,
        server_name="127.0.0.1",
        server_port=None,  # auto-pick a free port
        show_error=True,
        quiet=False,
    )
