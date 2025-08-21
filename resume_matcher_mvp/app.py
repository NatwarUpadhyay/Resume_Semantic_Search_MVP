import gradio as gr
import pandas as pd
import os
from datetime import datetime
import tempfile
from typing import List, Tuple

# Import custom modules
from src.document_parser import DocumentParser
from src.embeddings import EmbeddingEngine
from src.vector_db import VectorDatabase
from src.domain_classifier import DomainClassifier
from src.text_profile_parser import TextProfileParser
from sample_data.sample_jds import get_sample_jd, get_all_roles

class ResumeMatcherApp:
    def __init__(self):
        print("Initializing Resume Matcher Application...")
        
        # Initialize components
        self.parser = DocumentParser()
        self.embedding_engine = EmbeddingEngine()
        self.vector_db = VectorDatabase()
        self.domain_classifier = DomainClassifier()
        self.text_profile_parser = TextProfileParser()
        
        # Track uploaded files
        self.uploaded_files = []
        
        print("Application initialized successfully!")
    
    def upload_resumes(self, files) -> str:
        """Process uploaded resume files."""
        if not files:
            return "No files uploaded."
        
        results = []
        successful_uploads = 0
        
        for file in files:
            try:
                # Parse document
                text_content = self.parser.parse_file(file.name)
                
                if text_content:
                    # Classify domain
                    domain, conf, matched = self.domain_classifier.classify(text_content)
                    # Generate embedding
                    embedding = self.embedding_engine.generate_embedding(text_content)
                    
                    # Store in vector database
                    filename = os.path.basename(file.name)
                    resume_id = self.vector_db.store_resume(
                        filename=filename,
                        embedding=embedding,
                        text_content=text_content,
                        metadata={
                            "upload_timestamp": datetime.now().isoformat(),
                            "file_size": os.path.getsize(file.name),
                            "domain": domain,
                            "domain_confidence": conf,
                        }
                    )
                    
                    results.append(f"✅ {filename}: Successfully processed (domain: {domain}, conf {conf:.2f})")
                    successful_uploads += 1
                else:
                    results.append(f"❌ {filename}: Failed to extract text")
                    
            except Exception as e:
                filename = os.path.basename(file.name) if hasattr(file, 'name') else "Unknown"
                results.append(f"❌ {filename}: Error - {str(e)}")
        
        summary = f"Upload Summary: {successful_uploads}/{len(files)} files processed successfully.\n\n"
        return summary + "\n".join(results)
    
    def search_resumes(self, job_description: str, top_k: int, min_similarity: float, recruiter_query: str = "") -> Tuple[pd.DataFrame, str]:
        """Search for matching resumes based on job description."""
        if not job_description.strip() and not recruiter_query.strip():
            return pd.DataFrame(), "Please enter a job description."
        
        try:
            # Generate embedding for job description (fallback to recruiter query if JD empty)
            query_text = job_description.strip() if job_description.strip() else recruiter_query.strip()
            jd_embedding = self.embedding_engine.generate_embedding(query_text)

            # Domain filter from recruiter query if present
            where = None
            if recruiter_query.strip():
                domain, conf, _ = self.domain_classifier.classify(recruiter_query)
                if conf >= 0.4:
                    where = {"domain": domain}
            
            # Search similar resumes
            matches = self.vector_db.search_similar(
                query_embedding=jd_embedding,
                top_k=top_k,
                min_similarity=min_similarity,
                where=where
            )
            
            if not matches:
                return pd.DataFrame(), "No matches found. Try lowering the similarity threshold."
            
            # Convert to DataFrame for display
            df_data = []
            for match in matches:
                df_data.append({
                    "Rank": len(df_data) + 1,
                    "Filename": match["filename"],
                    "Similarity Score": f"{match['similarity']:.1%}",
                    "Content Preview": match["content_preview"],
                })
            
            df = pd.DataFrame(df_data)
            status = f"Found {len(matches)} matching resume(s)."
            
            return df, status
            
        except Exception as e:
            return pd.DataFrame(), f"Search error: {str(e)}"
    
    def load_sample_jd(self, role: str) -> str:
        """Load sample job description."""
        return get_sample_jd(role)

    def ingest_profile_text(self, raw_text: str) -> str:
        """Parse pasted unstructured profile text, classify domain, embed and store."""
        if not raw_text or not raw_text.strip():
            return "No text provided."
        parsed = self.text_profile_parser.parse(raw_text)
        domain, conf, matched = self.domain_classifier.classify(raw_text)
        embedding = self.embedding_engine.generate_embedding(raw_text)
        metadata = {
            "upload_timestamp": datetime.now().isoformat(),
            "source": "paste",
            "domain": domain,
            "domain_confidence": conf,
        }
        # Use synthetic filename for pasted entries
        self.vector_db.store_resume(
            filename=f"pasted_profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            embedding=embedding,
            text_content=raw_text,
            metadata=metadata,
        )
        return f"Profile ingested. Domain: {domain} (conf {conf:.2f}). Items parsed: education={len(parsed.get('education', []))}, projects={len(parsed.get('projects', []))}, experience={len(parsed.get('experience', []))}."
    
    def get_database_stats(self) -> str:
        """Get current database statistics."""
        stats = self.vector_db.get_collection_stats()
        return f"Database Status: {stats['total_resumes']} resumes stored"
    
    def clear_database(self) -> str:
        """Clear all data from database."""
        try:
            self.vector_db.clear_collection()
            return "Database cleared successfully!"
        except Exception as e:
            return f"Error clearing database: {str(e)}"

def create_interface():
    """Create and configure Gradio interface."""
    app = ResumeMatcherApp()
    
    with gr.Blocks(title="Resume-Job Matching System", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🎯 Resume-Job Matching Semantic Search")
        gr.Markdown("Upload resumes and find the best matches for your job descriptions using AI-powered semantic search.")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## 📁 Upload Resumes")
                
                file_upload = gr.File(
                    label="Select Resume Files",
                    file_count="multiple",
                    file_types=[".pdf", ".docx", ".txt"],
                    height=200
                )
                
                upload_btn = gr.Button("Process Resumes", variant="primary")
                upload_status = gr.Textbox(
                    label="Upload Status",
                    lines=6,
                    max_lines=10,
                    interactive=False
                )
                
                # Database controls
                gr.Markdown("## 🗄️ Database Controls")
                db_stats = gr.Textbox(
                    label="Database Status",
                    value=app.get_database_stats(),
                    interactive=False
                )
                
                with gr.Row():
                    refresh_stats_btn = gr.Button("Refresh Stats")
                    clear_db_btn = gr.Button("Clear Database", variant="stop")
            
            with gr.Column(scale=2):
                gr.Markdown("## 🔍 Job Description & Search")
                
                # Sample JD selection
                with gr.Row():
                    sample_role = gr.Dropdown(
                        choices=get_all_roles(),
                        label="Load Sample JD",
                        value="Software Engineer"
                    )
                    load_sample_btn = gr.Button("Load Sample")
                
                # Job description input
                job_description = gr.Textbox(
                    label="Job Description",
                    placeholder="Enter the job description or requirements...",
                    lines=8,
                    max_lines=15
                )

                # Recruiter NLP query input
                recruiter_query = gr.Textbox(
                    label="Recruiter NLP Query",
                    placeholder="e.g., MBA marketing Mumbai 2 years experience, SaaS product manager, ...",
                    lines=2,
                    max_lines=4
                )
                
                # Search parameters
                with gr.Row():
                    top_k = gr.Slider(
                        minimum=1,
                        maximum=20,
                        value=10,
                        step=1,
                        label="Number of Results"
                    )
                    min_similarity = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=0.3,
                        step=0.05,
                        label="Minimum Similarity"
                    )
                
                search_btn = gr.Button("🔍 Find Matches", variant="primary", size="lg")
        
        # Results section
        gr.Markdown("## 📊 Search Results")
        
        search_status = gr.Textbox(
            label="Search Status",
            interactive=False
        )
        
        results_table = gr.DataFrame(
            label="Matching Resumes",
            headers=["Rank", "Filename", "Similarity Score", "Content Preview"],
            datatype=["number", "str", "str", "str"],
            height=400
        )
        
        # Event handlers
        upload_btn.click(
            fn=app.upload_resumes,
            inputs=[file_upload],
            outputs=[upload_status]
        ).then(
            fn=app.get_database_stats,
            outputs=[db_stats]
        )
        
        search_btn.click(
            fn=app.search_resumes,
            inputs=[job_description, top_k, min_similarity, recruiter_query],
            outputs=[results_table, search_status]
        )
        
        load_sample_btn.click(
            fn=app.load_sample_jd,
            inputs=[sample_role],
            outputs=[job_description]
        )
        
        refresh_stats_btn.click(
            fn=app.get_database_stats,
            outputs=[db_stats]
        )
        
        clear_db_btn.click(
            fn=app.clear_database,
            outputs=[upload_status]
        ).then(
            fn=app.get_database_stats,
            outputs=[db_stats]
        )
        
        # Add usage instructions
        with gr.Accordion("📋 Usage Instructions", open=False):
            gr.Markdown("""
            ### How to Use:
            
            1. **Upload Resumes**: Select one or more resume files (PDF, DOCX, or TXT format)
            2. **Process Files**: Click "Process Resumes" to extract text and generate embeddings
            3. **Enter Job Description**: Type or paste a job description, or load a sample
            4. **Adjust Parameters**: Set the number of results and minimum similarity threshold
            5. **Search**: Click "Find Matches" to get ranked results
            6. **Review Results**: View similarity scores and resume previews
            
            ### Tips:
            - Upload multiple resumes for better comparison
            - Use detailed job descriptions for more accurate matching
            - Adjust similarity threshold based on your requirements
            - Higher similarity scores indicate better matches
            """)

        # Paste-text ingestion panel
        with gr.Accordion("🧩 Paste Candidate Text", open=False):
            pasted_text = gr.Textbox(
                label="Paste Unstructured Candidate Profile Text",
                placeholder="Paste candidate profile text here...",
                lines=10
            )
            ingest_btn = gr.Button("Ingest Profile Text", variant="secondary")
            ingest_status = gr.Textbox(label="Ingestion Status", interactive=False)
            ingest_btn.click(fn=app.ingest_profile_text, inputs=[pasted_text], outputs=[ingest_status])
    
    return interface

if __name__ == "__main__":
    # Create and launch interface
    interface = create_interface()
    interface.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
        quiet=False
    )
