import unittest
from unittest.mock import MagicMock

# Adjust the import path to work from the root of the project
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from resume_matcher_mvp.src.services.mapping_service import MappingService
from resume_matcher_mvp.src.core.text_profile_parser import TextProfileParser
from resume_matcher_mvp.src.core.domain_classifier import DomainClassifier


class TestMappingService(unittest.TestCase):

    def setUp(self):
        """Set up the test environment with mock objects."""
        # Create mock objects for the dependencies
        self.mock_parser = MagicMock(spec=TextProfileParser)
        self.mock_classifier = MagicMock(spec=DomainClassifier)

        # Instantiate the service with mocks
        self.mapping_service = MappingService(
            parser=self.mock_parser,
            classifier=self.mock_classifier
        )

    def test_map_profile_successful(self):
        """
        Test a successful mapping of a profile to a category and role.
        """
        # Arrange
        student_data = "I have experience in data analysis and python."
        jd_text = "We are looking for a data analyst with python skills."
        combined_text = student_data + "\n" + jd_text

        # Configure the mock classifier to return a specific category
        self.mock_classifier.classify.return_value = ("Analytics", 0.9, ["analytics", "python"])

        # Act
        category, role, confidence, keywords = self.mapping_service.map_profile(student_data, jd_text)

        # Assert
        # Check that the classifier was called correctly
        self.mock_classifier.classify.assert_called_once_with(combined_text)

        # Check that the results are as expected
        self.assertEqual(category, "Analytics")
        # The role should be 'Business Analytics' as it's the first in the list and "analytics" is in the text
        self.assertEqual(role, "Business Analytics")
        self.assertEqual(confidence, 0.9)
        self.assertEqual(keywords, ["analytics", "python"])

    def test_map_profile_general_category(self):
        """
        Test the behavior when the classifier returns a 'general' category.
        """
        # Arrange
        student_data = "Some generic text."
        jd_text = "A generic job description."
        combined_text = student_data + "\n" + jd_text

        # Configure the mock to return 'general'
        self.mock_classifier.classify.return_value = ("general", 0.1, [])

        # Act
        category, role, confidence, keywords = self.mapping_service.map_profile(student_data, jd_text)

        # Assert
        self.mock_classifier.classify.assert_called_once_with(combined_text)
        self.assertEqual(category, "general")
        self.assertEqual(role, "N/A")
        self.assertEqual(confidence, 0.1)

    def test_map_profile_empty_input(self):
        """
        Test the behavior with empty input strings.
        """
        # Act
        category, role, confidence, keywords = self.mapping_service.map_profile("", "")

        # Assert
        self.assertEqual(category, "N/A")
        self.assertEqual(role, "N/A")
        self.assertEqual(confidence, 0.0)
        # Ensure the classifier is not called with empty strings
        self.mock_classifier.classify.assert_not_called()


if __name__ == "__main__":
    unittest.main()
