import unittest
from unittest.mock import patch, Mock

from app.model.ai_service.ai_ticket_service import AITicketService


class TestAITicketService(unittest.TestCase):
    def test_create_ticket(self):
        # Arrange
        input_text = "Sample input text"
        service = AITicketService()

        # Act
        ticket_dict = service.create_ticket(input_text)

        # Assert
        self.assertIsInstance(ticket_dict, dict)
        self.assertIn("title", ticket_dict)
        self.assertIn("location", ticket_dict)

    @patch("app.ai_ticket_service.pipeline")
    def test_generate_title(self, mock_pipeline):
        # Arrange
        input_text = "Sample input text"
        service = AITicketService()
        mock_pipeline.return_value = Mock(
            return_value=[{"generated_text": "Generated Title"}]
        )

        # Act
        generated_title = service.generate_title(input_text)

        # Assert
        self.assertEqual(generated_title, "Generated Title")

    @patch("app.ai_ticket_service.pipeline")
    def test_generate_affected_person(self, mock_pipeline):
        # Arrange
        input_text = "Sample input text"
        service = AITicketService()
        mock_pipeline.return_value = Mock(
            return_value=[{"entity": "B-PER", "word": "John"}]
        )

        # Act
        generated_person = service.generate_affected_person(input_text)

        # Assert
        self.assertEqual(generated_person, "John")

    @patch("app.ai_ticket_service.pipeline")
    def test_generate_keywords(self, mock_pipeline):
        # Arrange
        input_text = "Sample input text"
        service = AITicketService()
        mock_pipeline.return_value = Mock(
            return_value=[{"entity": "KEY", "word": "Keyword"}]
        )

        # Act
        generated_keywords = service.generate_keywords(input_text)

        # Assert
        self.assertEqual(generated_keywords, ["Keyword"])
