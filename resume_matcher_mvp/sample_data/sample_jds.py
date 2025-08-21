SAMPLE_JOB_DESCRIPTIONS = {
    "Software Engineer": """
We are looking for a Software Engineer to join our team.

Requirements:
- 3+ years of experience in Python or Java
- Experience with web frameworks (Django, Flask, Spring)
- Knowledge of databases (SQL, NoSQL)
- Experience with cloud platforms (AWS, GCP, Azure)
- Strong problem-solving skills
- Bachelor's degree in Computer Science or related field

Responsibilities:
- Develop and maintain web applications
- Collaborate with cross-functional teams
- Write clean, maintainable code
- Participate in code reviews
- Debug and resolve technical issues
""",
    
    "Data Scientist": """
Join our data science team to drive insights from complex datasets.

Requirements:
- Master's degree in Data Science, Statistics, or related field
- 2+ years of experience in machine learning
- Proficiency in Python/R and SQL
- Experience with ML frameworks (scikit-learn, TensorFlow, PyTorch)
- Knowledge of statistical analysis and modeling
- Experience with data visualization tools
- Strong analytical and communication skills

Responsibilities:
- Build predictive models and algorithms
- Analyze large datasets to extract insights
- Collaborate with business stakeholders
- Present findings to leadership team
- Deploy models into production
""",

    "Marketing Manager": """
We're seeking a Marketing Manager to lead our marketing initiatives.

Requirements:
- 5+ years of marketing experience
- Experience with digital marketing campaigns
- Knowledge of SEO/SEM and social media marketing
- Strong analytical skills with experience in marketing analytics
- Excellent written and verbal communication
- Experience managing marketing budgets
- Bachelor's degree in Marketing or related field

Responsibilities:
- Develop and execute marketing strategies
- Manage marketing campaigns across multiple channels
- Analyze campaign performance and ROI
- Lead a team of marketing specialists
- Collaborate with sales and product teams
""",

    "Product Manager": """
Looking for a Product Manager to drive product strategy and development.

Requirements:
- 4+ years of product management experience
- Experience with agile development methodologies
- Strong analytical and data-driven decision making
- Experience with user research and testing
- Knowledge of product analytics tools
- Excellent communication and leadership skills
- Technical background preferred

Responsibilities:
- Define product roadmap and strategy
- Work with engineering teams on product development
- Conduct user research and gather feedback
- Analyze product metrics and user behavior
- Coordinate with cross-functional teams
"""
}

def get_sample_jd(role: str) -> str:
    """Get sample job description by role."""
    return SAMPLE_JOB_DESCRIPTIONS.get(role, SAMPLE_JOB_DESCRIPTIONS["Software Engineer"])

def get_all_roles() -> list:
    """Get list of all available sample roles."""
    return list(SAMPLE_JOB_DESCRIPTIONS.keys())
