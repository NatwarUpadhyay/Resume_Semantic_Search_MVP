import re
from typing import Dict, List, Tuple

from .roles import ROLE_CATEGORIES


class DomainClassifier:
    """
    Rule-based domain classifier that maps text to a predefined Profile Category.
    It uses keyword matching to determine the most relevant category and provides
    a confidence score.
    """

    def __init__(self) -> None:
        """Initializes the classifier with domain keywords."""
        self.domain_keywords: Dict[str, List[str]] = {
            "Analytics": [
                "analytics", "data", "visualization", "bi", "power bi", "tableau", "sql",
                "python", "r", "statistics", "modeling", "dashboard", "reporting",
                "data analysis", "business intelligence"
            ],
            "Capital Markets": [
                "equity", "research", "investment", "banking", "risk", "management",
                "finance", "valuation", "derivatives", "trading", "fixed income", "portfolio",
                "capital markets"
            ],
            "Corporate Finance": [
                "finance", "corporate finance", "accounting", "tax", "audit", "p&l",
                "balance sheet", "cash flow", "financial planning", "fp&a", "financial operations"
            ],
            "Human Resources": [
                "hr", "human resources", "recruitment", "talent acquisition", "onboarding",
                "employee relations", "compensation", "benefits", "hiring", "hr generalist"
            ],
            "Marketing": [
                "marketing", "digital marketing", "seo", "sem", "content", "social media",
                "brand", "campaign", "market research", "product marketing", "performance marketing",
                "category management"
            ],
            "Operations": [
                "operations", "supply chain", "logistics", "procurement", "inventory",
                "customer success", "service delivery", "process improvement", "six sigma",
                "service operations"
            ],
            "Sales": [
                "sales", "b2b", "b2c", "business development", "account management", "bfsi",
                "channel sales", "tech sales", "revenue", "quota", "lead generation"
            ],
            "Strategy": [
                "strategy", "consulting", "business research", "corporate strategy",
                "market analysis", "competitive intelligence", "due diligence", "business case",
                "roadmap", "business consulting"
            ],
            "Technology": [
                "technology", "it", "product management", "project management", "business analyst",
                "presales", "tech consulting", "agile", "scrum", "jira", "sprint",
                "software development", "it project management"
            ],
        }

        # Ensure all role categories have keywords
        for category in ROLE_CATEGORIES:
            if category not in self.domain_keywords:
                self.domain_keywords[category] = []

        self.tokenizer = re.compile(r"[a-zA-Z][a-zA-Z+#/.&-]+")

    def _normalize(self, text: str) -> str:
        """Converts text to lowercase for case-insensitive matching."""
        return text.lower()

    def classify(self, text: str) -> Tuple[str, float, List[str]]:
        """
        Classifies the input text into one of the domains.

        Args:
            text: The text to classify (e.g., student profile or job description).

        Returns:
            A tuple containing:
            - The best-matched domain (str).
            - A confidence score (float).
            - A list of matched keywords (list[str]).
        """
        if not text or not text.strip():
            return "general", 0.0, []

        text_norm = self._normalize(text)
        tokens = set(self.tokenizer.findall(text_norm))

        def count_matches(keywords: List[str]) -> Tuple[int, List[str]]:
            """Counts keyword occurrences in the text."""
            matched: List[str] = []
            score = 0
            for kw in keywords:
                kw_l = kw.lower()
                # Give higher weight to multi-word phrases
                if " " in kw_l:
                    if kw_l in text_norm:
                        score += 2
                        matched.append(kw)
                elif kw_l in tokens:
                    score += 1
                    matched.append(kw)
            return score, matched

        domain_scores: Dict[str, int] = {}
        domain_matches: Dict[str, List[str]] = {}
        total_score = 0

        for domain, kws in self.domain_keywords.items():
            s, m = count_matches(kws)
            domain_scores[domain] = s
            domain_matches[domain] = m
            total_score += s

        if total_score == 0:
            return "general", 0.0, []

        # Find the domain with the highest score
        best_domain = max(domain_scores, key=lambda d: domain_scores[d])
        best_score = domain_scores[best_domain]
        matched_keywords = domain_matches[best_domain]

        # Calculate confidence as the proportion of the best domain's score to the total score
        confidence = float(best_score) / total_score if total_score > 0 else 0.0

        return best_domain, confidence, matched_keywords
