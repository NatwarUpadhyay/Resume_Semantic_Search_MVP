import re
from typing import Dict, List, Tuple


class DomainClassifier:
    """Rule-based domain classifier with simple keyword matching and confidence scoring.

    Returns a tuple: (domain, confidence, matched_keywords)
    - domain: str like "technology", "finance", "marketing", "operations", "consulting", "data_science", "product", "hr", or "general"
    - confidence: float in [0,1]
    - matched_keywords: list of matched tokens for debugging/audit
    """

    def __init__(self) -> None:
        self.domain_keywords: Dict[str, List[str]] = {
            "technology": [
                "python", "java", "c++", "javascript", "django", "flask", "spring", "aws", "gcp", "azure",
                "microservices", "api", "mulesoft", "sql", "nosql", "devops", "kubernetes", "docker", "cloud",
                "backend", "frontend", "full stack", "sdet", "data engineer"
            ],
            "data_science": [
                "machine learning", "deep learning", "pytorch", "tensorflow", "scikit-learn", "xgboost",
                "random forest", "regression", "nlp", "computer vision", "data science", "analytics", "feature",
                "model", "predictive", "segmentation", "forecasting"
            ],
            "finance": [
                "finance", "financial", "credit", "investment", "valuation", "cash flow", "equity", "debt",
                "balance sheet", "p&l", "risk", "derivatives", "insurance", "actuarial", "pricing"
            ],
            "marketing": [
                "marketing", "seo", "sem", "campaign", "brand", "content", "social media", "google ads",
                "paid", "roi", "crm", "email marketing", "market research"
            ],
            "operations": [
                "operations", "supply chain", "logistics", "inventory", "procurement", "lean", "six sigma",
                "process", "automation", "kaizen", "quality"
            ],
            "consulting": [
                "consulting", "stakeholder", "strategy", "business case", "transformation", "roadmap",
                "workshop", "client engagement", "advisory"
            ],
            "product": [
                "product", "roadmap", "backlog", "user stories", "pm", "prd", "market fit", "go-to-market",
                "feature prioritization", "a/b", "analytics"
            ],
            "hr": [
                "recruitment", "talent", "hr", "hiring", "onboarding", "performance", "l&d", "compensation",
                "benefits"
            ],
        }

        # Precompile regex for tokenization
        self.tokenizer = re.compile(r"[a-zA-Z][a-zA-Z+#/.&-]+")

    def _normalize(self, text: str) -> str:
        return text.lower()

    def classify(self, text: str) -> Tuple[str, float, List[str]]:
        if not text or not text.strip():
            return "general", 0.0, []

        text_norm = self._normalize(text)
        tokens = set(self.tokenizer.findall(text_norm))

        # Also consider multiword phrases by substring search
        def count_matches(keywords: List[str]) -> Tuple[int, List[str]]:
            matched: List[str] = []
            score = 0
            for kw in keywords:
                kw_l = kw.lower()
                if " " in kw_l:
                    if kw_l in text_norm:
                        score += 2
                        matched.append(kw)
                else:
                    if kw_l in tokens:
                        score += 1
                        matched.append(kw)
            return score, matched

        domain_scores: Dict[str, int] = {}
        domain_matches: Dict[str, List[str]] = {}
        max_possible = 0
        for domain, kws in self.domain_keywords.items():
            # Estimate an upper bound for normalization
            max_possible = max(max_possible, len(kws) * 2)
            s, m = count_matches(kws)
            domain_scores[domain] = s
            domain_matches[domain] = m

        best_domain = max(domain_scores, key=domain_scores.get)
        best_score = domain_scores[best_domain]
        matched_keywords = domain_matches[best_domain]

        # Confidence scaled against rough upper bound and simple thresholding
        confidence = 0.0 if max_possible == 0 else min(1.0, best_score / (0.25 * max_possible) )

        if best_score == 0:
            return "general", 0.2, []

        return best_domain, float(confidence), matched_keywords


