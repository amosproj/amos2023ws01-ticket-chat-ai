import sys
import os

# determine the absolute path to the 'backend' directory
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# add the directory 'backend/app/email/' to sys.path
sys.path.append(os.path.join(backend_path, "app", "email"))

from app.email.main import run_proxy
import app.email.handle_mail as hm
import pytest
import imaplib
import smtplib
from unittest.mock import patch, MagicMock
from test.config.pytest import SKIP_TEST


class TestEmailProxy:
    def email_proxy(self, monkeypatch):
        # Mocking EmailProxy
        class MockEmailProxy:
            def __init__(self, imap_server, smtp_server, email_address, password):
                self.imap_server = imap_server
                self.smtp_server = smtp_server
                self.email_address = email_address
                self.password = password

            def __enter__(self):
                return self

            def spin(self):
                return [1]

            def process_mail(self, msg_num):
                return (self.email_address, "Test Subject", "Test Content")

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

        # Apply the mock to EmailProxy in the module
        monkeypatch.setattr(
            "app.email.emailProxy.EmailProxy", MockEmailProxy
        )

        # Return an instance of the mock
        return MockEmailProxy(
            "mock_imap_server", "mock_smtp_server", "mock_email_address", "mock_password"
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

    def test_imap_reconnect(self):
        # Mocking the EmailProxy and SmtpConnection classes
        with patch("app.email.emailProxy.EmailProxy") as mock_email_proxy:
            # Mocking the IMAP connection to raise an exception on the first attempt
            mock_imap = MagicMock()
            mock_imap.search.side_effect = imaplib.IMAP4.abort()
            mock_email_proxy.return_value = mock_imap

            # Running the run_proxy function
            with pytest.raises(Exception) as e:
                run_proxy()

            # Verifying that try_reconnect was called only if the initial connection was successful
            if mock_imap.start_connection.called:
                mock_imap.try_reconnect.assert_called_once()

                # Check if the reconnect was successful
                assert mock_imap.try_reconnect.return_value
            else:
                assert not mock_imap.try_reconnect.called

    def test_smtp_reconnect(self):
        # Mocking the EmailProxy and SmtpConnection classes
        with patch("app.email.smtp_conn.SmtpConnection") as mock_smtp_conn:
            # Mocking the SMTP connection to raise an exception on the first attempt
            mock_smtp = MagicMock()
            mock_smtp.send_mail.side_effect = smtplib.SMTPServerDisconnected(
                "Connection lost"
            )
            mock_smtp_conn.return_value = mock_smtp

            # Running the run_proxy function
            with pytest.raises(Exception) as e:
                run_proxy()

            # Verifying that try_reconnect was called only if the initial connection was successful
            if mock_smtp.start_connection.called:
                mock_smtp.try_reconnect.assert_called_once()

                # Check if the reconnect was successful
                assert mock_smtp.try_reconnect.return_value
            else:
                assert not mock_smtp.try_reconnect.called
