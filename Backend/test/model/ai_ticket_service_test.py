import unittest
from unittest.mock import MagicMock

from app.model.ai_ticket_service.ai_ticket_service import AITicketService


class TestAITicketService(unittest.TestCase):
    def setUp(self):
        self.ai_ticket_service = AITicketService()

        # Existing mocks
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

        # Mocks for category
        self.mock_category_pipeline = MagicMock()
        self.ai_ticket_service.category_generator_pipe = self.mock_category_pipeline

        # Mock for service
        self.mock_service_pipeline = MagicMock()
        self.ai_ticket_service.service_generator_pipe = self.mock_service_pipeline

        # Mock for priority
        self.mock_priority_pipeline = MagicMock()
        self.ai_ticket_service.priority_generator_pipe = self.mock_priority_pipeline

    def test_create_ticket(self):
        # Arrange
        input_text = "Sample input text"
        service = AITicketService()

        # Act
        ticket_dict = service.create_ticket(input_text, "")

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
        email = ""

        # Act
        self.ai_ticket_service.generate_affected_person(input_text, email, ticket_dict)

        # Assert
        self.assertEqual(ticket_dict["affectedPerson"], "John")

    def test_generate_prediction_success(self):
        # Arrange
        input_text = "Sample input text for a successful prediction"
        ticket_dict = {}
        field = "category"
        field_values = self.ai_ticket_service.category_values

        # Mocking the pipeline to return a high confidence prediction
        self.mock_category_pipeline.return_value = [{"label": "LABEL_0", "score": 0.9}]
        self.ai_ticket_service.category_generator_pipe = self.mock_category_pipeline

        # Act
        self.ai_ticket_service.generate_prediction(
            input_text,
            self.ai_ticket_service.category_generator_pipe,
            field,
            field_values,
            ticket_dict,
        )

        # Assert
        self.assertEqual(
            ticket_dict[field], field_values[0]
        )  # Assuming LABEL_0 maps to the first category

    def test_generate_prediction_low_confidence(self):
        # Arrange
        input_text = "Sample input text for a low confidence prediction"
        ticket_dict = {}
        field = "service"
        field_values = self.ai_ticket_service.service_values

        # Mocking the pipeline to return a low confidence prediction
        self.mock_service_pipeline.return_value = [{"label": "LABEL_1", "score": 0.4}]
        self.ai_ticket_service.service_generator_pipe = self.mock_service_pipeline

        # Act
        self.ai_ticket_service.generate_prediction(
            input_text,
            self.ai_ticket_service.service_generator_pipe,
            field,
            field_values,
            ticket_dict,
        )

        # Assert
        self.assertIsNone(ticket_dict[field])

    def test_generate_prediction_empty_output(self):
        # Arrange
        input_text = "Sample input text for an empty prediction"
        ticket_dict = {}
        field = "priority"
        field_values = self.ai_ticket_service.priority_values

        # Mocking the pipeline to return an empty output
        self.mock_priority_pipeline.return_value = []
        self.ai_ticket_service.priority_generator_pipe = self.mock_priority_pipeline

        # Act
        self.ai_ticket_service.generate_prediction(
            input_text,
            self.ai_ticket_service.priority_generator_pipe,
            field,
            field_values,
            ticket_dict,
        )

        # Assert
        self.assertIsNone(ticket_dict[field])
