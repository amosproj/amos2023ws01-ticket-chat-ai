import sys
import os

# determine the absolute path to the 'backend' directory
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

# add the directory 'backend/app/email/' to sys.path
sys.path.append(os.path.join(backend_path, 'app', 'email'))

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
from unittest.mock import patch, MagicMock

load_dotenv()
password = os.getenv("PASSWORD")
config = configparser.ConfigParser()
config.read("config.ini")
imap_server = config["DEFAULT"]["IMAP_SERVER"]
smtp_server = config["DEFAULT"]["SMTP_SERVER"]
email_address = config["DEFAULT"]["EMAIL_ADDRESS"]


def test_email():
    # test sending emails
    with SmtpConnection(smtp_server, email_address, password) as smtp_service:
        assert isinstance(smtp_service, SmtpConnection)

        test_subject = "Test Subject"
        test_content = "Test Content"
        test_mail = hm.make_email(
            email_address, email_address, test_subject, test_content
        )
        assert smtp_service.send_mail(test_mail)

    with EmailProxy(imap_server, smtp_server, email_address, password) as proxy:
        # check if the class has been constructed
        assert isinstance(proxy, EmailProxy)

        # check if we got a message
        time.sleep(10)
        msg_nums = proxy.spin()
        assert msg_nums[-1]

        # check if the message we received was the same as the one we send
        msg_num = msg_nums[-1]
        sender, subject, content = proxy.process_mail(msg_num)
        assert sender == email_address
        assert subject == test_subject
        assert content == test_content

    # check if the connection got closed
    with pytest.raises(imaplib.IMAP4.error):
        proxy.imap.check()

def test_imap_reconnect():
    # mocking the EmailProxy and SmtpConnection classes
    with patch("app.email.emailProxy.EmailProxy") as mock_email_proxy:
        # mocking the IMAP connection to raise an exception on the first attempt
        mock_imap = MagicMock()
        mock_imap.search.side_effect = imaplib.IMAP4.abort()
        mock_email_proxy.return_value = mock_imap

        # running the run_proxy function
        with pytest.raises(Exception) as e:
            run_proxy()

        # verifying that try_reconnect was called only if the initial connection was successful
        if mock_imap.start_connection.called:
            mock_imap.try_reconnect.assert_called_once()

            # Check if the reconnect was successful
            assert mock_imap.try_reconnect.return_value
        else:
            assert not mock_imap.try_reconnect.called

def test_smtp_reconnect():
    # mocking the EmailProxy and SmtpConnection classes
    with patch("app.email.smtp_conn.SmtpConnection") as mock_smtp_conn:
        # mocking the SMTP connection to raise an exception on the first attempt
        mock_smtp = MagicMock()
        mock_smtp.send_mail.side_effect = smtplib.SMTPServerDisconnected("Connection lost")
        mock_smtp_conn.return_value = mock_smtp

         # running the run_proxy function
        with pytest.raises(Exception) as e:
            run_proxy()

        # verifying that try_reconnect was called only if the initial connection was successful
        if mock_smtp.start_connection.called:
            mock_smtp.try_reconnect.assert_called_once()

            # Check if the reconnect was successful
            assert mock_smtp.try_reconnect.return_value
        else:
            assert not mock_smtp.try_reconnect.called