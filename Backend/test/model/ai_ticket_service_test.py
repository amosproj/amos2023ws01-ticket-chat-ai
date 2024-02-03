import unittest
from unittest.mock import MagicMock

from app.model.ai_ticket_service.ai_ticket_service import AITicketService


class TestAITicketService(unittest.TestCase):
    def setUp(self):
        self.ai_ticket_service = AITicketService()

        self.mock_title_pipeline = MagicMock()
        self.mock_title_pipeline.return_value = [{"generated_text": "Mocked Title"}]
        self.ai_ticket_service.title_generator_pipe = self.mock_title_pipeline

        self.mock_affected_person_pipeline = MagicMock()
        self.mock_affected_person_pipeline.return_value = [
            {"entity": "B-PER", "word": "John"}
        ]
        self.ai_ticket_service.affected_person_generator_pipe = (
            self.mock_affected_person_pipeline
        )

        self.mock_keywords_pipeline = MagicMock()
        self.mock_keywords_pipeline.return_value = [
            {"entity": "KEY", "word": "Keyword"}
        ]
        self.ai_ticket_service.generate_keywords = self.mock_keywords_pipeline

    def test_create_ticket(self):
        # Arrange
        input_text = "Sample input text"
        service = AITicketService()

        # Act
        ticket_dict = service.create_ticket(input_text)

        # Assert
        self.assertIsInstance(ticket_dict, dict)
        self.assertIn("title", ticket_dict)
        self.assertIn("service", ticket_dict)

    def test_generate_title(self):
        # Arrange
        input_text = "Test Input Text"
        ticket_dict = {}

        # Act
        self.ai_ticket_service.generate_title(input_text, ticket_dict)

        # Assert
        self.assertEqual(ticket_dict["title"], "Mocked Title")

    def test_generate_affected_person(self):
        # Arrange
        input_text = "Sample input text"
        ticket_dict = {}

        # Act
        self.ai_ticket_service.generate_affected_person(
            input_text, ticket_dict
        )

        # Assert
        self.assertEqual(ticket_dict["affectedPerson"], "John")
