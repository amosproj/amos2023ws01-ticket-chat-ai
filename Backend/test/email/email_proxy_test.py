import os
import sys


# determine the absolute path to the 'backend' directory
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# add the directory 'backend/app/email/' to sys.path
sys.path.append(os.path.join(backend_path, "app", "email"))

from app.email.main import run_proxy
import app.email.handle_mail as hm
from emailProxy import EmailProxy
from smtp_conn import SmtpConnection
import pytest
import imaplib
import smtplib
from unittest.mock import patch, MagicMock
from test.config.pytest import SKIP_TEST


class TestEmailProxy:
    def email_proxy(self, monkeypatch):
        # Mocking EmailProxy
        class MockEmailProxy:
            def __init__(
                self,
                imap_server,
                smtp_server,
                email_address,
                password,
                blacklisted_emails,
            ):
                self.imap_server = imap_server
                self.smtp_server = smtp_server
                self.email_address = email_address
                self.password = password
                self.blacklisted_emails = blacklisted_emails

            def __enter__(self):
                return self

            def spin(self):
                return [1]

            def process_mail(self, msg_num):
                return (self.email_address, "Test Subject", "Test Content")

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

        # Apply the mock to EmailProxy in the module
        monkeypatch.setattr("app.email.emailProxy.EmailProxy", MockEmailProxy)

        # Return an instance of the mock
        return MockEmailProxy(
            "mock_imap_server",
            "mock_smtp_server",
            "mock_email_address",
            "mock_password",
            [],
        )

    def test_email_proxy(self, monkeypatch):
        email_proxy = self.email_proxy(monkeypatch)

        assert email_proxy.imap_server == "mock_imap_server"
        assert email_proxy.smtp_server == "mock_smtp_server"
        assert email_proxy.email_address == "mock_email_address"
        assert email_proxy.password == "mock_password"

        msg_nums = email_proxy.spin()
        assert msg_nums == [1]

        sender, subject, content = email_proxy.process_mail(msg_nums[0])
        assert sender == "mock_email_address"
        assert subject == "Test Subject"
        assert content == "Test Content"

    @pytest.fixture
    def mock_imap(self):
        with patch("imaplib.IMAP4_SSL") as mock:
            instance = mock.return_value
            instance.login.return_value = "OK"
            instance.select.return_value = "OK"
            # Simulate a connection drop and successful reconnection
            instance.search.side_effect = [imaplib.IMAP4.abort(), ("OK", ["1"])]
            instance.fetch.return_value = ("OK", [b"Email data"])
            yield instance

    @pytest.fixture
    def mock_smtp(self):
        with patch("smtplib.SMTP") as mock:
            instance = mock.return_value
            # Simulate a connection drop and successful reconnection
            instance.send_message.side_effect = [smtplib.SMTPServerDisconnected(), None]
            instance.login.return_value = "OK"
            instance.starttls.return_value = "OK"
            yield instance

    def test_imap_reconnect(self, mock_imap, mock_smtp):
        # Create an instance of EmailProxy
        proxy = EmailProxy(
            "imap.example.com", "smtp.example.com", "test@example.com", "password", []
        )

        with proxy:
            # Spin the proxy to process emails
            msg_nums = proxy.spin()
            # Check if IMAP login was called twice due to reconnect
            assert msg_nums == ["1"]
            assert mock_imap.login.call_count == 2

    def test_smtp_reconnect(self, mock_smtp):
        # Create an instance of SmtpConnection
        connection = SmtpConnection(
            "smtp.example.com", "test@example.com", "password", MagicMock()
        )

        with connection:
            # Send a message to test reconnect functionality
            connection.send_mail(MagicMock())
            # Check if SMTP login was called twice due to reconnect
            assert mock_smtp.login.call_count == 2
