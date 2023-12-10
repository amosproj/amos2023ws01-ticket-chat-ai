import sys
import os

# determine the absolute path to the 'backend' directory
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# add the directory 'backend/app/email/' to sys.path
sys.path.append(os.path.join(backend_path, "app", "email_router"))

import pytest
from unittest.mock import patch
from app.email_router.smtp_conn import SmtpConnection
from test.config.pytest import SKIP_TEST
from app.email_router.email_service import EmailService


class TestSmtpConnection:
    @patch("smtplib.SMTP")
    def test_send_mail(self, mock_smtp):
        smtp_connection = SmtpConnection("mock_smtp_server", "mock_email_address", "mock_email_password")

        smtp_connection.start_connection() 

        message = "Test Message"
        smtp_connection.send_mail(message)

        # Check whether the send_message method of the mocked SMTP object has been called
        mock_smtp.return_value.send_message.assert_called_once_with(message)

class TestEmailService:
    def smtp_connection(self, monkeypatch):
        # Mocking SmtpConnection
        class MockSmtpConnection:
            def __init__(self, smtp_server, email_address, email_password):
                self.smtp_server = smtp_server
                self.email_address = email_address
                self.email_password = email_password

            def __enter__(self):
                return self

            def start_connection(self):
                pass

            def try_reconnect(self):
                pass

            def send_mail(self, message):
                self.mail_sent = True

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

        # Apply the mock to SmtpConnection in the module
        monkeypatch.setattr("app.email_router.email_service.SmtpConnection", MockSmtpConnection)

        # Return an instance of the mock
        return MockSmtpConnection("mock_smtp_server", "mock_email_address", "mock_email_password")
    
    def test_smtp_connection(self, monkeypatch):
        smtp_connection = self.smtp_connection(monkeypatch)

        assert smtp_connection.smtp_server == "mock_smtp_server"
        assert smtp_connection.email_address == "mock_email_address"
        assert smtp_connection.email_password == "mock_email_password"

    def test_send_email(self, monkeypatch):
        smtp_connection = self.smtp_connection(monkeypatch)
        email_service = EmailService(smtp_conn=smtp_connection)

        sender = "test_sender@example.com"
        subject = "Test Subject"
        content = "Test Content"

        email_service.send_email(sender, subject, content)

        assert smtp_connection.mail_sent

    def test_make_email(self, monkeypatch):
        smtp_connection = self.smtp_connection(monkeypatch)
        email_service = EmailService(smtp_conn=smtp_connection)

        to_address = "test_receiver@example.com"
        subject = "Test Subject"
        message = "Test Message"

        email_message = email_service.make_email(to_address, subject, message)

        assert email_message["from"] == smtp_connection.email_address
        assert email_message["to"] == to_address
        assert email_message["Subject"] == subject
        assert email_message.get_content().replace('\r\n', '\n') == message + '\n'
