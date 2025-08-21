"""
Enhanced Role Mapping System with detailed role descriptions and domain context.
This module provides comprehensive role definitions, skills, and domain mappings
for better candidate-job matching.
"""

from typing import Dict, List, Tuple, Optional
import re
from dataclasses import dataclass


@dataclass
class RoleInfo:
    """Detailed information about a specific role."""
    title: str
    category: str
    domain: str
    description: str
    key_skills: List[str]
    typical_responsibilities: List[str]
    experience_levels: List[str]
    keywords: List[str]


class RoleMapper:
    """Enhanced role mapping system with comprehensive role definitions."""
    
    def __init__(self):
        self.roles_db = self._initialize_roles_database()
        self.category_domains = self._initialize_category_domains()
        
    def _initialize_category_domains(self) -> Dict[str, str]:
        """Map categories to their primary domains."""
        return {
            "Analytics": "data_science",
            "Capital Markets": "finance",
            "Corporate Finance": "finance", 
            "Human Resources": "hr",
            "Marketing": "marketing",
            "Operations": "operations",
            "Sales": "sales",
            "Strategy": "consulting",
            "Technology": "technology"
        }
    
    def _initialize_roles_database(self) -> Dict[str, RoleInfo]:
        """Initialize comprehensive roles database with detailed information."""
        
        roles = {}
        
        # Analytics Roles
        roles["Business Analytics"] = RoleInfo(
            title="Business Analytics",
            category="Analytics", 
            domain="data_science",
            description="Analyzes business data to identify trends, patterns, and insights that drive strategic decision-making and operational improvements.",
            key_skills=["SQL", "Excel", "Python", "R", "Tableau", "Power BI", "Statistical Analysis", "Data Visualization", "Business Intelligence"],
            typical_responsibilities=[
                "Analyze business performance metrics and KPIs",
                "Create dashboards and reports for stakeholders", 
                "Identify trends and patterns in business data",
                "Provide data-driven recommendations for business improvements",
                "Collaborate with cross-functional teams on analytics projects"
            ],
            experience_levels=["Entry", "Mid", "Senior"],
            keywords=["analytics", "business intelligence", "data analysis", "reporting", "dashboards", "metrics", "kpi"]
        )
        
        roles["Data Visualisation"] = RoleInfo(
            title="Data Visualisation",
            category="Analytics",
            domain="data_science", 
            description="Specializes in creating compelling visual representations of complex data to communicate insights effectively to stakeholders.",
            key_skills=["Tableau", "Power BI", "D3.js", "Python", "R", "Excel", "Design Principles", "Storytelling", "Dashboard Design"],
            typical_responsibilities=[
                "Design and develop interactive dashboards and reports",
                "Transform complex data into clear visual narratives",
                "Collaborate with analysts and stakeholders on visualization requirements",
                "Ensure data accuracy and visual consistency across platforms",
                "Train users on dashboard usage and interpretation"
            ],
            experience_levels=["Entry", "Mid", "Senior"],
            keywords=["visualization", "tableau", "power bi", "dashboards", "charts", "graphs", "visual design"]
        )
        
        # Capital Markets Roles
        roles["Equity Research"] = RoleInfo(
            title="Equity Research",
            category="Capital Markets",
            domain="finance",
            description="Conducts in-depth analysis of companies and industries to provide investment recommendations and market insights to institutional clients.",
            key_skills=["Financial Modeling", "Valuation", "Industry Analysis", "Excel", "Bloomberg", "Financial Statements Analysis", "Report Writing"],
            typical_responsibilities=[
                "Analyze company financials and industry trends",
                "Build financial models and perform valuations",
                "Write research reports with investment recommendations", 
                "Present findings to institutional clients and portfolio managers",
                "Monitor market developments and update investment thesis"
            ],
            experience_levels=["Associate", "VP", "Director"],
            keywords=["equity research", "financial modeling", "valuation", "investment", "bloomberg", "analyst reports"]
        )
        
        roles["Investment Banking"] = RoleInfo(
            title="Investment Banking",
            category="Capital Markets", 
            domain="finance",
            description="Provides financial advisory services including M&A, capital raising, and strategic transactions for corporate and institutional clients.",
            key_skills=["Financial Modeling", "Valuation", "M&A Analysis", "Pitch Deck Creation", "Excel", "PowerPoint", "Due Diligence"],
            typical_responsibilities=[
                "Execute M&A transactions and capital raising activities",
                "Build complex financial models and perform valuations",
                "Prepare pitch materials and client presentations",
                "Conduct due diligence and market research",
                "Support senior bankers in client relationship management"
            ],
            experience_levels=["Analyst", "Associate", "VP", "Director"],
            keywords=["investment banking", "m&a", "mergers", "acquisitions", "capital markets", "ipo", "debt", "equity"]
        )
        
        roles["Risk Management"] = RoleInfo(
            title="Risk Management", 
            category="Capital Markets",
            domain="finance",
            description="Identifies, assesses, and mitigates financial and operational risks across trading, investment, and business operations.",
            key_skills=["Risk Analytics", "VaR Models", "Stress Testing", "Python", "R", "SQL", "Regulatory Knowledge", "Quantitative Analysis"],
            typical_responsibilities=[
                "Develop and maintain risk measurement models",
                "Monitor portfolio risk exposures and limits",
                "Conduct stress testing and scenario analysis",
                "Prepare risk reports for senior management and regulators",
                "Implement risk management policies and procedures"
            ],
            experience_levels=["Analyst", "Associate", "VP", "Director"],
            keywords=["risk management", "var", "stress testing", "credit risk", "market risk", "operational risk"]
        )
        
        # Corporate Finance Roles
        roles["Business Finance"] = RoleInfo(
            title="Business Finance",
            category="Corporate Finance",
            domain="finance", 
            description="Manages financial planning, analysis, and decision-making to support business operations and strategic initiatives.",
            key_skills=["Financial Planning", "Budgeting", "Forecasting", "Excel", "Financial Analysis", "Variance Analysis", "Business Partnering"],
            typical_responsibilities=[
                "Develop annual budgets and quarterly forecasts",
                "Analyze financial performance and variances",
                "Support business decision-making with financial insights",
                "Partner with business units on financial planning",
                "Prepare management reports and presentations"
            ],
            experience_levels=["Analyst", "Senior Analyst", "Manager"],
            keywords=["financial planning", "budgeting", "forecasting", "fp&a", "business finance", "variance analysis"]
        )
        
        roles["Financial Operations"] = RoleInfo(
            title="Financial Operations",
            category="Corporate Finance",
            domain="finance",
            description="Manages day-to-day financial operations including accounting, reporting, and process optimization to ensure accurate and timely financial information.",
            key_skills=["Accounting", "Financial Reporting", "ERP Systems", "Process Improvement", "Excel", "SAP", "Oracle", "GAAP Knowledge"],
            typical_responsibilities=[
                "Oversee monthly and quarterly financial close processes",
                "Ensure compliance with accounting standards and regulations", 
                "Manage accounts payable, receivable, and general ledger",
                "Implement process improvements and automation",
                "Support external audits and regulatory reporting"
            ],
            experience_levels=["Analyst", "Senior Analyst", "Manager"],
            keywords=["financial operations", "accounting", "financial reporting", "close process", "erp", "gaap"]
        )
        
        roles["Tax and Accounting"] = RoleInfo(
            title="Tax and Accounting",
            category="Corporate Finance", 
            domain="finance",
            description="Manages tax compliance, planning, and accounting functions to ensure regulatory compliance and optimize tax efficiency.",
            key_skills=["Tax Compliance", "Tax Planning", "Accounting Standards", "Excel", "Tax Software", "Research Skills", "Regulatory Knowledge"],
            typical_responsibilities=[
                "Prepare and review tax returns and compliance filings",
                "Conduct tax planning and optimization strategies",
                "Ensure compliance with local and international tax regulations",
                "Support tax audits and inquiries from authorities",
                "Research tax implications of business transactions"
            ],
            experience_levels=["Staff", "Senior", "Manager"],
            keywords=["tax", "accounting", "compliance", "tax planning", "tax returns", "regulations"]
        )
        
        # Human Resources Roles  
        roles["HR Generalist"] = RoleInfo(
            title="HR Generalist",
            category="Human Resources",
            domain="hr",
            description="Provides comprehensive HR support across multiple functions including recruitment, employee relations, performance management, and policy administration.",
            key_skills=["HR Policies", "Employee Relations", "Performance Management", "HRIS", "Communication", "Problem Solving", "Legal Compliance"],
            typical_responsibilities=[
                "Support recruitment and onboarding processes",
                "Handle employee relations issues and grievances",
                "Administer performance management programs",
                "Ensure compliance with employment laws and regulations",
                "Develop and update HR policies and procedures"
            ],
            experience_levels=["Coordinator", "Generalist", "Senior Generalist"],
            keywords=["hr generalist", "employee relations", "performance management", "hr policies", "compliance"]
        )
        
        roles["Talent Acquisition"] = RoleInfo(
            title="Talent Acquisition",
            category="Human Resources",
            domain="hr", 
            description="Specializes in sourcing, attracting, and hiring top talent to meet organizational staffing needs and strategic objectives.",
            key_skills=["Recruiting", "Sourcing", "Interviewing", "ATS Systems", "LinkedIn Recruiting", "Employer Branding", "Candidate Assessment"],
            typical_responsibilities=[
                "Develop and execute recruiting strategies for open positions",
                "Source candidates through various channels and networks",
                "Conduct interviews and assess candidate qualifications",
                "Manage candidate experience throughout hiring process",
                "Partner with hiring managers on role requirements and selection"
            ],
            experience_levels=["Recruiter", "Senior Recruiter", "Lead Recruiter"],
            keywords=["talent acquisition", "recruiting", "sourcing", "hiring", "ats", "linkedin recruiting"]
        )
        
        # Marketing Roles
        roles["Category Management"] = RoleInfo(
            title="Category Management", 
            category="Marketing",
            domain="marketing",
            description="Manages product categories to optimize assortment, pricing, and merchandising strategies that drive sales and profitability.",
            key_skills=["Category Analysis", "Market Research", "Pricing Strategy", "Vendor Management", "Excel", "Data Analysis", "Negotiation"],
            typical_responsibilities=[
                "Analyze category performance and market trends",
                "Develop category strategies and assortment plans",
                "Negotiate with suppliers and manage vendor relationships",
                "Optimize pricing and promotional strategies",
                "Monitor competitive landscape and consumer insights"
            ],
            experience_levels=["Analyst", "Manager", "Senior Manager"],
            keywords=["category management", "merchandising", "pricing", "vendor management", "assortment"]
        )
        
        roles["Digital Marketing"] = RoleInfo(
            title="Digital Marketing",
            category="Marketing",
            domain="marketing",
            description="Develops and executes digital marketing campaigns across online channels to drive brand awareness, engagement, and conversions.",
            key_skills=["SEO/SEM", "Social Media Marketing", "Google Analytics", "PPC", "Content Marketing", "Email Marketing", "Marketing Automation"],
            typical_responsibilities=[
                "Plan and execute digital marketing campaigns",
                "Manage social media presence and content strategy", 
                "Optimize website and content for search engines",
                "Analyze campaign performance and ROI metrics",
                "Coordinate with creative teams on digital assets"
            ],
            experience_levels=["Specialist", "Manager", "Senior Manager"],
            keywords=["digital marketing", "seo", "sem", "social media", "ppc", "google ads", "content marketing"]
        )
        
        roles["Market Research"] = RoleInfo(
            title="Market Research",
            category="Marketing", 
            domain="marketing",
            description="Conducts research to understand market trends, consumer behavior, and competitive landscape to inform business and marketing strategies.",
            key_skills=["Research Methodology", "Survey Design", "Statistical Analysis", "SPSS", "Excel", "Data Interpretation", "Report Writing"],
            typical_responsibilities=[
                "Design and conduct market research studies",
                "Analyze consumer behavior and market trends",
                "Prepare research reports with actionable insights",
                "Present findings to stakeholders and leadership",
                "Monitor competitive intelligence and industry developments"
            ],
            experience_levels=["Analyst", "Senior Analyst", "Manager"],
            keywords=["market research", "consumer insights", "surveys", "statistical analysis", "competitive intelligence"]
        )
        
        roles["Marketing Management"] = RoleInfo(
            title="Marketing Management",
            category="Marketing",
            domain="marketing", 
            description="Leads marketing strategy development and execution to drive brand growth, customer acquisition, and market share expansion.",
            key_skills=["Marketing Strategy", "Brand Management", "Campaign Management", "Budget Management", "Team Leadership", "Analytics"],
            typical_responsibilities=[
                "Develop comprehensive marketing strategies and plans",
                "Lead cross-functional marketing campaigns and initiatives",
                "Manage marketing budgets and resource allocation",
                "Oversee brand positioning and messaging strategies",
                "Analyze market performance and adjust strategies accordingly"
            ],
            experience_levels=["Manager", "Senior Manager", "Director"],
            keywords=["marketing management", "marketing strategy", "brand management", "campaign management"]
        )
        
        roles["Performance Marketing"] = RoleInfo(
            title="Performance Marketing",
            category="Marketing",
            domain="marketing",
            description="Focuses on data-driven marketing campaigns that deliver measurable results and ROI through digital advertising and optimization.",
            key_skills=["PPC Management", "Conversion Optimization", "A/B Testing", "Google Ads", "Facebook Ads", "Analytics", "Attribution Modeling"],
            typical_responsibilities=[
                "Manage paid advertising campaigns across digital platforms",
                "Optimize campaigns for performance metrics and ROI",
                "Conduct A/B tests to improve conversion rates",
                "Analyze attribution and customer journey data",
                "Report on campaign performance and recommendations"
            ],
            experience_levels=["Specialist", "Manager", "Senior Manager"],
            keywords=["performance marketing", "ppc", "conversion optimization", "google ads", "facebook ads", "roi"]
        )
        
        # Operations Roles
        roles["Customer Success"] = RoleInfo(
            title="Customer Success",
            category="Operations",
            domain="operations",
            description="Ensures customer satisfaction, retention, and growth by proactively managing customer relationships and driving product adoption.",
            key_skills=["Customer Relationship Management", "CRM Software", "Communication", "Problem Solving", "Data Analysis", "Project Management"],
            typical_responsibilities=[
                "Manage customer onboarding and implementation processes",
                "Monitor customer health scores and usage metrics",
                "Proactively identify and address customer issues",
                "Drive product adoption and expansion opportunities",
                "Collaborate with sales and product teams on customer feedback"
            ],
            experience_levels=["Associate", "Manager", "Senior Manager"],
            keywords=["customer success", "customer retention", "customer satisfaction", "crm", "onboarding"]
        )
        
        roles["Service Operations"] = RoleInfo(
            title="Service Operations", 
            category="Operations",
            domain="operations",
            description="Manages service delivery operations to ensure efficient, high-quality service provision and customer satisfaction.",
            key_skills=["Operations Management", "Process Improvement", "Quality Management", "Service Level Management", "Data Analysis"],
            typical_responsibilities=[
                "Oversee day-to-day service delivery operations",
                "Monitor service quality and performance metrics",
                "Implement process improvements and efficiency initiatives",
                "Manage service level agreements and customer expectations",
                "Coordinate with cross-functional teams on service issues"
            ],
            experience_levels=["Analyst", "Manager", "Senior Manager"],
            keywords=["service operations", "service delivery", "process improvement", "quality management", "sla"]
        )
        
        roles["Supply Chain Management"] = RoleInfo(
            title="Supply Chain Management",
            category="Operations", 
            domain="operations",
            description="Manages end-to-end supply chain operations including procurement, logistics, inventory management, and vendor relationships.",
            key_skills=["Supply Chain Planning", "Inventory Management", "Procurement", "Logistics", "Vendor Management", "ERP Systems"],
            typical_responsibilities=[
                "Develop and execute supply chain strategies",
                "Manage inventory levels and demand forecasting",
                "Oversee procurement processes and vendor relationships",
                "Optimize logistics and distribution networks",
                "Implement supply chain improvements and cost reductions"
            ],
            experience_levels=["Analyst", "Manager", "Director"],
            keywords=["supply chain", "procurement", "inventory management", "logistics", "vendor management"]
        )
        
        # Sales Roles
        roles["B2B Sales"] = RoleInfo(
            title="B2B Sales",
            category="Sales",
            domain="sales",
            description="Manages business-to-business sales processes, building relationships with corporate clients to drive revenue growth.",
            key_skills=["B2B Sales", "Relationship Building", "Negotiation", "CRM", "Sales Process", "Account Management", "Presentation Skills"],
            typical_responsibilities=[
                "Identify and pursue new business opportunities",
                "Build and maintain relationships with key decision makers",
                "Manage sales pipeline and forecast revenue",
                "Negotiate contracts and close deals",
                "Collaborate with internal teams on customer solutions"
            ],
            experience_levels=["Representative", "Manager", "Director"],
            keywords=["b2b sales", "business development", "account management", "enterprise sales", "relationship building"]
        )
        
        roles["B2C Sales"] = RoleInfo(
            title="B2C Sales", 
            category="Sales",
            domain="sales",
            description="Focuses on direct-to-consumer sales, managing customer interactions and transactions to drive individual customer purchases.",
            key_skills=["Customer Service", "Sales Techniques", "Product Knowledge", "CRM", "Communication", "Closing Skills"],
            typical_responsibilities=[
                "Engage with individual customers to understand needs",
                "Present products and services to potential customers",
                "Process sales transactions and handle customer inquiries",
                "Meet individual and team sales targets",
                "Maintain customer relationships for repeat business"
            ],
            experience_levels=["Associate", "Representative", "Manager"],
            keywords=["b2c sales", "retail sales", "customer service", "direct sales", "consumer sales"]
        )
        
        roles["BFSI Sales"] = RoleInfo(
            title="BFSI Sales",
            category="Sales", 
            domain="sales",
            description="Specializes in selling banking, financial services, and insurance products to individual and corporate clients.",
            key_skills=["Financial Products Knowledge", "Regulatory Compliance", "Relationship Management", "Risk Assessment", "Sales Process"],
            typical_responsibilities=[
                "Sell banking and financial products to clients",
                "Assess client financial needs and recommend solutions",
                "Ensure compliance with financial regulations",
                "Build long-term client relationships",
                "Meet sales targets for financial products"
            ],
            experience_levels=["Associate", "Manager", "Senior Manager"],
            keywords=["bfsi sales", "banking sales", "financial services", "insurance sales", "wealth management"]
        )
        
        roles["Channel Sales"] = RoleInfo(
            title="Channel Sales",
            category="Sales",
            domain="sales", 
            description="Manages indirect sales through partner channels, distributors, and resellers to expand market reach and drive revenue.",
            key_skills=["Channel Management", "Partner Relationship Management", "Sales Enablement", "Channel Strategy", "Negotiation"],
            typical_responsibilities=[
                "Develop and manage channel partner relationships",
                "Create channel sales strategies and programs",
                "Provide sales support and training to partners",
                "Monitor channel performance and resolve conflicts",
                "Expand partner network and market coverage"
            ],
            experience_levels=["Manager", "Senior Manager", "Director"],
            keywords=["channel sales", "partner management", "indirect sales", "distributor management", "reseller"]
        )
        
        roles["Technology Sales"] = RoleInfo(
            title="Technology Sales",
            category="Sales",
            domain="sales",
            description="Sells technology products and solutions, requiring deep technical knowledge to address complex customer requirements.",
            key_skills=["Technical Sales", "Solution Selling", "Product Demos", "Technical Presentations", "CRM", "Consultative Selling"],
            typical_responsibilities=[
                "Understand customer technical requirements and challenges",
                "Present and demonstrate technology solutions",
                "Collaborate with technical teams on solution design",
                "Manage complex sales cycles and stakeholder relationships",
                "Provide technical expertise throughout sales process"
            ],
            experience_levels=["Representative", "Manager", "Director"],
            keywords=["technology sales", "solution selling", "technical sales", "software sales", "saas sales"]
        )
        
        # Strategy Roles
        roles["Business Consulting"] = RoleInfo(
            title="Business Consulting",
            category="Strategy",
            domain="consulting",
            description="Provides strategic advice and solutions to help organizations improve performance, solve complex problems, and achieve business objectives.",
            key_skills=["Strategic Analysis", "Problem Solving", "Presentation Skills", "Project Management", "Industry Knowledge", "Client Management"],
            typical_responsibilities=[
                "Analyze client business challenges and opportunities",
                "Develop strategic recommendations and implementation plans",
                "Lead client engagements and project teams",
                "Present findings and recommendations to senior executives",
                "Support change management and transformation initiatives"
            ],
            experience_levels=["Analyst", "Consultant", "Manager", "Partner"],
            keywords=["business consulting", "strategy consulting", "management consulting", "transformation", "advisory"]
        )
        
        roles["Business Research"] = RoleInfo(
            title="Business Research", 
            category="Strategy",
            domain="consulting",
            description="Conducts comprehensive research and analysis to support strategic decision-making and business development initiatives.",
            key_skills=["Research Methodology", "Data Analysis", "Industry Analysis", "Competitive Intelligence", "Report Writing", "Presentation Skills"],
            typical_responsibilities=[
                "Conduct market and industry research studies",
                "Analyze competitive landscape and trends",
                "Gather and synthesize information from multiple sources",
                "Prepare research reports and presentations",
                "Support strategic planning and decision-making processes"
            ],
            experience_levels=["Analyst", "Senior Analyst", "Manager"],
            keywords=["business research", "market analysis", "competitive intelligence", "industry research", "strategic research"]
        )
        
        roles["Corporate Strategy"] = RoleInfo(
            title="Corporate Strategy",
            category="Strategy",
            domain="consulting", 
            description="Develops and executes corporate-level strategies including M&A, portfolio optimization, and long-term strategic planning.",
            key_skills=["Strategic Planning", "Financial Modeling", "M&A Analysis", "Portfolio Management", "Market Analysis", "Executive Communication"],
            typical_responsibilities=[
                "Develop corporate strategy and long-term planning",
                "Evaluate M&A opportunities and strategic partnerships",
                "Analyze business portfolio and optimization opportunities",
                "Support board and executive decision-making",
                "Monitor strategy execution and performance"
            ],
            experience_levels=["Analyst", "Manager", "Director", "VP"],
            keywords=["corporate strategy", "strategic planning", "m&a", "portfolio management", "business strategy"]
        )
        
        # Technology Roles
        roles["IT Business Analyst"] = RoleInfo(
            title="IT Business Analyst",
            category="Technology",
            domain="technology",
            description="Bridges business and IT by analyzing business requirements and translating them into technical specifications and solutions.",
            key_skills=["Requirements Analysis", "Business Process Modeling", "SQL", "System Analysis", "Documentation", "Stakeholder Management"],
            typical_responsibilities=[
                "Gather and analyze business requirements for IT projects",
                "Create functional specifications and system documentation",
                "Facilitate communication between business and technical teams",
                "Support system testing and user acceptance testing",
                "Ensure solutions meet business needs and objectives"
            ],
            experience_levels=["Analyst", "Senior Analyst", "Lead Analyst"],
            keywords=["business analyst", "requirements analysis", "system analysis", "functional specifications", "it projects"]
        )
        
        roles["IT PreSales"] = RoleInfo(
            title="IT PreSales", 
            category="Technology",
            domain="technology",
            description="Provides technical expertise during the sales process, helping to design solutions and demonstrate technical capabilities to prospects.",
            key_skills=["Technical Presentations", "Solution Design", "Product Knowledge", "Customer Engagement", "Proposal Writing", "Demo Skills"],
            typical_responsibilities=[
                "Support sales teams with technical expertise and demonstrations",
                "Design technical solutions based on customer requirements",
                "Conduct product demonstrations and proof of concepts",
                "Respond to technical aspects of RFPs and proposals",
                "Build relationships with technical stakeholders at prospects"
            ],
            experience_levels=["Engineer", "Senior Engineer", "Manager"],
            keywords=["presales", "solution engineering", "technical sales", "product demos", "solution design"]
        )
        
        roles["IT Project Management"] = RoleInfo(
            title="IT Project Management",
            category="Technology",
            domain="technology", 
            description="Manages IT projects from initiation to completion, ensuring delivery on time, within budget, and meeting quality requirements.",
            key_skills=["Project Management", "Agile/Scrum", "Risk Management", "Stakeholder Management", "Budget Management", "Team Leadership"],
            typical_responsibilities=[
                "Plan, execute, and deliver IT projects successfully",
                "Manage project scope, timeline, budget, and resources",
                "Coordinate cross-functional teams and stakeholders",
                "Identify and mitigate project risks and issues",
                "Ensure project deliverables meet quality standards"
            ],
            experience_levels=["Coordinator", "Manager", "Senior Manager"],
            keywords=["project management", "it projects", "agile", "scrum", "pmp", "delivery management"]
        )
        
        roles["Product Management"] = RoleInfo(
            title="Product Management",
            category="Technology",
            domain="product",
            description="Defines product strategy, roadmap, and features to deliver products that meet market needs and business objectives.",
            key_skills=["Product Strategy", "Roadmap Planning", "User Research", "Data Analysis", "Agile Methodologies", "Stakeholder Management"],
            typical_responsibilities=[
                "Define product vision, strategy, and roadmap",
                "Gather and prioritize product requirements",
                "Work with engineering teams on product development",
                "Analyze market trends and competitive landscape",
                "Measure product performance and user feedback"
            ],
            experience_levels=["Associate PM", "PM", "Senior PM", "Director"],
            keywords=["product management", "product strategy", "roadmap", "user research", "product development"]
        )
        
        roles["Tech Consulting"] = RoleInfo(
            title="Tech Consulting",
            category="Technology", 
            domain="consulting",
            description="Provides technology consulting services to help organizations implement, optimize, and transform their technology capabilities.",
            key_skills=["Technology Strategy", "System Integration", "Digital Transformation", "Cloud Technologies", "Enterprise Architecture"],
            typical_responsibilities=[
                "Assess client technology needs and capabilities",
                "Design technology solutions and implementation strategies",
                "Lead technology transformation projects",
                "Provide expertise on emerging technologies and trends",
                "Support change management for technology initiatives"
            ],
            experience_levels=["Consultant", "Senior Consultant", "Manager", "Partner"],
            keywords=["technology consulting", "digital transformation", "system integration", "cloud consulting", "enterprise architecture"]
        )
        
        return roles
    
    def get_role_info(self, role_title: str) -> Optional[RoleInfo]:
        """Get detailed information for a specific role."""
        return self.roles_db.get(role_title)
    
    def get_all_roles(self) -> List[str]:
        """Get list of all available roles."""
        return list(self.roles_db.keys())
    
    def get_roles_by_category(self, category: str) -> List[str]:
        """Get all roles in a specific category."""
        return [role for role, info in self.roles_db.items() if info.category == category]
    
    def get_roles_by_domain(self, domain: str) -> List[str]:
        """Get all roles in a specific domain."""
        return [role for role, info in self.roles_db.items() if info.domain == domain]
    
    def find_matching_roles(self, text: str, top_k: int = 5) -> List[Tuple[str, float, str]]:
        """Find roles that best match the given text based on keywords and skills."""
        text_lower = text.lower()
        role_scores = []
        
        for role_title, role_info in self.roles_db.items():
            score = 0
            matched_terms = []
            
            # Check keywords
            for keyword in role_info.keywords:
                if keyword.lower() in text_lower:
                    score += 2
                    matched_terms.append(keyword)
            
            # Check skills
            for skill in role_info.key_skills:
                if skill.lower() in text_lower:
                    score += 1.5
                    matched_terms.append(skill)
            
            # Check responsibilities (partial matching)
            for resp in role_info.typical_responsibilities:
                resp_words = resp.lower().split()
                for word in resp_words:
                    if len(word) > 3 and word in text_lower:
                        score += 0.5
                        break
            
            if score > 0:
                confidence = min(1.0, score / 10)  # Normalize to 0-1
                role_scores.append((role_title, confidence, ", ".join(matched_terms[:5])))
        
        # Sort by score and return top_k
        role_scores.sort(key=lambda x: x[1], reverse=True)
        return role_scores[:top_k]
    
    def get_role_context(self, role_title: str) -> str:
        """Get formatted context information for a role."""
        role_info = self.get_role_info(role_title)
        if not role_info:
            return f"Role '{role_title}' not found in database."
        
        context = f"""
**{role_info.title}** ({role_info.category} - {role_info.domain})

**Description:** {role_info.description}

**Key Skills:** {', '.join(role_info.key_skills[:8])}

**Typical Responsibilities:**
{chr(10).join(f'• {resp}' for resp in role_info.typical_responsibilities[:4])}

**Experience Levels:** {', '.join(role_info.experience_levels)}
        """.strip()
        
        return context


# Example usage and testing
if __name__ == "__main__":
    mapper = RoleMapper()
    
    # Test role matching
    sample_text = "I have experience in Python, SQL, data analysis, and creating dashboards with Tableau"
    matches = mapper.find_matching_roles(sample_text)
    
    print("Top matching roles:")
    for role, confidence, terms in matches:
        print(f"- {role}: {confidence:.2f} (matched: {terms})")
    
    # Test role context
    print("\n" + "="*50)
    print(mapper.get_role_context("Business Analytics"))