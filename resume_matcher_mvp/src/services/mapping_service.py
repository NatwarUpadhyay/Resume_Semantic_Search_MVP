import re
from typing import Tuple, List, Dict

from ..core.text_profile_parser import TextProfileParser
from ..core.domain_classifier import DomainClassifier
from ..core.roles import ROLE_CATEGORIES


class MappingService:
    """
    Service to map student profiles and job descriptions to a Profile Category and Role.
    """

    def __init__(self, parser: TextProfileParser, classifier: DomainClassifier):
        """
        Initializes the service with a text parser and a domain classifier.

        Args:
            parser: An instance of TextProfileParser.
            classifier: An instance of DomainClassifier.
        """
        self.parser = parser
        self.classifier = classifier

    def map_profile(self, student_data_text: str, jd_text: str) -> Tuple[str, str, float, List[str]]:
        """
        Maps the student and job description to the best-fit category and role.

        Args:
            student_data_text: The raw text of the student's profile.
            jd_text: The raw text of the job description.

        Returns:
            A tuple containing:
            - The matched Profile Category (str).
            - The matched Role (str).
            - The confidence score for the category match (float).
            - The keywords that contributed to the category match (list[str]).
        """
        if not student_data_text.strip() or not jd_text.strip():
            return "N/A", "N/A", 0.0, []

        # Combine student and JD text for a holistic classification
        combined_text = student_data_text + "\n" + jd_text

        # 1. Classify to get the Profile Category
        category, confidence, matched_keywords = self.classifier.classify(combined_text)

        if category == "general":
            return "general", "N/A", confidence, []

        # 2. Determine the best Role within the matched Category
        possible_roles = ROLE_CATEGORIES.get(category, [])
        if not possible_roles:
            return category, "N/A", confidence, matched_keywords

        best_role = self._find_best_role(combined_text, possible_roles)

        return category, best_role, confidence, matched_keywords

    def _find_best_role(self, text: str, roles: List[str]) -> str:
        """
        Finds the best role from a list of possible roles based on keyword matching.

        Args:
            text: The combined text of the student profile and JD.
            roles: A list of possible roles for a given category.

        Returns:
            The best-matched role (str).
        """
        text_lower = text.lower()
        role_scores: Dict[str, int] = {role: 0 for role in roles}

        for role in roles:
            # Create keywords from the role name itself
            keywords = re.findall(r'\w+', role.lower())

            # Simple stemming for "analytics"
            if "analytics" in keywords:
                keywords.extend(["analysis", "analyst"])

            for keyword in keywords:
                if keyword in text_lower:
                    role_scores[role] += 1

        # Find the role with the highest score
        if any(role_scores.values()):
            # In case of a tie, the first role encountered with the max score is chosen.
            best_role = max(role_scores, key=role_scores.get)
            return best_role

        # If no keywords match, return the first role as a default
        return roles[0]
