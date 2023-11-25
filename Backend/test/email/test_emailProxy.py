import sys
import os

# determine the absolute path to the 'backend' directory
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# add the directory 'backend/app/email/' to sys.path
sys.path.append(os.path.join(backend_path, "app", "email"))

from app.email.emailProxy import EmailProxy
from app.email.smtp_conn import SmtpConnection
from app.email.main import run_proxy
import app.email.handle_mail as hm
from dotenv import load_dotenv, find_dotenv

import pytest
import configparser
import imaplib
import smtplib
import time
import unittest
from unittest.mock import patch, MagicMock
from test.config.pytest import SKIP_TEST

load_dotenv()
password = os.getenv("PASSWORD")
config = configparser.ConfigParser()
config.read("config.ini")
imap_server = config["DEFAULT"]["IMAP_SERVER"]
smtp_server = config["DEFAULT"]["SMTP_SERVER"]
email_address = config["DEFAULT"]["EMAIL_ADDRESS"]


@pytest.mark.skipif(condition=SKIP_TEST, reason="Github cant connect, works local")
class EmailProxyTest(unittest.TestCase):
    def test_email(self):
        # Test sending emails
        with SmtpConnection(smtp_server, email_address, password) as smtp_service:
            self.assertIsInstance(smtp_service, SmtpConnection)

            test_subject = "Test Subject"
            test_content = "Test Content"
            test_mail = hm.make_email(
                email_address, email_address, test_subject, test_content
            )
            self.assertTrue(smtp_service.send_mail(test_mail))

        with EmailProxy(imap_server, smtp_server, email_address, password) as proxy:
            # Check if the class has been constructed
            self.assertIsInstance(proxy, EmailProxy)

            # Check if we got a message
            time.sleep(10)
            msg_nums = proxy.spin()
            self.assertTrue(msg_nums[-1])

            # Check if the message we received was the same as the one we sent
            msg_num = msg_nums[-1]
            sender, subject, content = proxy.process_mail(msg_num)
            self.assertEqual(sender, email_address)
            self.assertEqual(subject, test_subject)
            self.assertEqual(content, test_content)

        # Check if the connection got closed
        with self.assertRaises(imaplib.IMAP4.error):
            proxy.imap.check()

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
                self.assertTrue(mock_imap.try_reconnect.return_value)
            else:
                self.assertFalse(mock_imap.try_reconnect.called)

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
                self.assertTrue(mock_smtp.try_reconnect.return_value)
            else:
                self.assertFalse(mock_smtp.try_reconnect.called)
