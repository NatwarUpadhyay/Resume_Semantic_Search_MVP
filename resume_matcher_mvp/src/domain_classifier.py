import re
from typing import Dict, List, Tuple, Optional


class DomainClassifier:
    """Enhanced domain classifier with comprehensive keyword matching and role-aware classification.

    Returns a tuple: (domain, confidence, matched_keywords)
    - domain: str like "technology", "finance", "marketing", "operations", "consulting", "data_science", "product", "hr", "sales", or "general"
    - confidence: float in [0,1]
    - matched_keywords: list of matched tokens for debugging/audit
    """

    def __init__(self) -> None:
        self.domain_keywords: Dict[str, List[str]] = {
            "technology": [
                "python", "java", "c++", "javascript", "django", "flask", "spring", "aws", "gcp", "azure",
                "microservices", "api", "mulesoft", "sql", "nosql", "devops", "kubernetes", "docker", "cloud",
                "backend", "frontend", "full stack", "sdet", "data engineer", "software", "programming",
                "development", "coding", "technical", "system", "database", "server", "web development",
                "mobile development", "agile", "scrum", "git", "ci/cd", "automation", "testing", "qa"
            ],
            "data_science": [
                "machine learning", "deep learning", "pytorch", "tensorflow", "scikit-learn", "xgboost",
                "random forest", "regression", "nlp", "computer vision", "data science", "analytics", "feature",
                "model", "predictive", "segmentation", "forecasting", "statistics", "statistical analysis",
                "data mining", "big data", "hadoop", "spark", "tableau", "power bi", "visualization",
                "business intelligence", "kpi", "metrics", "dashboard", "reporting", "insights"
            ],
            "finance": [
                "finance", "financial", "credit", "investment", "valuation", "cash flow", "equity", "debt",
                "balance sheet", "p&l", "risk", "derivatives", "insurance", "actuarial", "pricing",
                "banking", "capital markets", "trading", "portfolio", "hedge fund", "private equity",
                "m&a", "mergers", "acquisitions", "ipo", "bonds", "securities", "compliance", "audit",
                "accounting", "gaap", "ifrs", "tax", "budgeting", "forecasting", "fp&a", "treasury"
            ],
            "marketing": [
                "marketing", "seo", "sem", "campaign", "brand", "content", "social media", "google ads",
                "paid", "roi", "crm", "email marketing", "market research", "digital marketing",
                "advertising", "promotion", "branding", "customer acquisition", "lead generation",
                "conversion", "engagement", "reach", "impressions", "ctr", "cpc", "cpm", "attribution",
                "funnel", "segmentation", "targeting", "personalization", "automation", "growth hacking"
            ],
            "operations": [
                "operations", "supply chain", "logistics", "inventory", "procurement", "lean", "six sigma",
                "process", "automation", "kaizen", "quality", "manufacturing", "production", "efficiency",
                "optimization", "workflow", "sop", "continuous improvement", "vendor management",
                "cost reduction", "capacity planning", "demand planning", "distribution", "warehousing",
                "fulfillment", "customer service", "service delivery", "sla", "performance metrics"
            ],
            "consulting": [
                "consulting", "stakeholder", "strategy", "business case", "transformation", "roadmap",
                "workshop", "client engagement", "advisory", "strategic planning", "change management",
                "process improvement", "organizational design", "business analysis", "requirements",
                "solution design", "implementation", "project management", "delivery", "methodology",
                "best practices", "benchmarking", "assessment", "recommendations", "presentations"
            ],
            "product": [
                "product", "roadmap", "backlog", "user stories", "pm", "prd", "market fit", "go-to-market",
                "feature prioritization", "a/b", "analytics", "product management", "product development",
                "user experience", "ux", "ui", "design", "prototyping", "wireframes", "user research",
                "customer feedback", "product strategy", "launch", "iteration", "mvp", "agile", "scrum"
            ],
            "hr": [
                "recruitment", "talent", "hr", "hiring", "onboarding", "performance", "l&d", "compensation",
                "benefits", "human resources", "talent acquisition", "recruiting", "sourcing", "interviewing",
                "employee relations", "performance management", "training", "development", "succession planning",
                "workforce planning", "diversity", "inclusion", "culture", "engagement", "retention",
                "payroll", "hris", "policies", "compliance", "labor relations"
            ],
            "sales": [
                "sales", "selling", "revenue", "quota", "target", "pipeline", "lead", "prospect", "customer",
                "client", "account", "relationship", "negotiation", "closing", "deal", "contract",
                "b2b", "b2c", "enterprise", "smb", "channel", "partner", "distributor", "reseller",
                "territory", "hunter", "farmer", "cold calling", "warm leads", "referrals", "networking",
                "presentation", "demo", "proposal", "rfp", "win rate", "conversion", "upsell", "cross-sell"
            ]
        }

        # Role-specific keywords for better classification
        self.role_keywords: Dict[str, str] = {
            "business analyst": "consulting",
            "data analyst": "data_science", 
            "financial analyst": "finance",
            "marketing analyst": "marketing",
            "sales representative": "sales",
            "product manager": "product",
            "software engineer": "technology",
            "data scientist": "data_science",
            "operations manager": "operations",
            "hr generalist": "hr",
            "recruiter": "hr",
            "consultant": "consulting",
            "developer": "technology",
            "engineer": "technology"
        }

        # Precompile regex for tokenization
        self.tokenizer = re.compile(r"[a-zA-Z][a-zA-Z+#/.&-]+")

    def _normalize(self, text: str) -> str:
        return text.lower()

    def _check_role_keywords(self, text_norm: str) -> Optional[str]:
        """Check for specific role mentions that can directly indicate domain."""
        for role, domain in self.role_keywords.items():
            if role in text_norm:
                return domain
        return None

    def classify(self, text: str) -> Tuple[str, float, List[str]]:
        if not text or not text.strip():
            return "general", 0.0, []

        text_norm = self._normalize(text)
        tokens = set(self.tokenizer.findall(text_norm))

        # First check for direct role mentions
        direct_domain = self._check_role_keywords(text_norm)

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

        # If we found a direct role match, boost that domain's score
        if direct_domain and direct_domain in domain_scores:
            domain_scores[direct_domain] += 5
            if domain_scores[direct_domain] > best_score:
                best_domain = direct_domain
                best_score = domain_scores[direct_domain]
                matched_keywords = domain_matches[direct_domain] + ["role_match"]

        # Enhanced confidence calculation
        if best_score == 0:
            return "general", 0.2, []

        # Improved confidence scaling
        base_confidence = min(1.0, best_score / (0.2 * max_possible))
        
        # Boost confidence for direct role matches
        if direct_domain == best_domain:
            base_confidence = min(1.0, base_confidence + 0.3)
        
        # Boost confidence for multiple strong matches
        if best_score >= 5:
            base_confidence = min(1.0, base_confidence + 0.2)

        return best_domain, float(base_confidence), matched_keywords

    def get_domain_description(self, domain: str) -> str:
        """Get a description of what the domain encompasses."""
        descriptions = {
            "technology": "Software development, IT systems, cloud computing, and technical roles",
            "data_science": "Data analysis, machine learning, business intelligence, and analytics",
            "finance": "Banking, investment, accounting, financial planning, and capital markets",
            "marketing": "Digital marketing, brand management, advertising, and customer acquisition",
            "operations": "Supply chain, logistics, process improvement, and operational efficiency",
            "consulting": "Strategic advisory, business transformation, and management consulting",
            "product": "Product management, development, user experience, and go-to-market strategy",
            "hr": "Human resources, talent acquisition, employee relations, and workforce management",
            "sales": "Revenue generation, customer relationships, business development, and account management",
            "general": "Mixed or unclear domain classification"
        }
        return descriptions.get(domain, "Unknown domain")