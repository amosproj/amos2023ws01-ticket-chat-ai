from app.email.emailProxy import EmailProxy
from app.email.smtp import SmtpConnection
import app.email.handle_mail as hm
from dotenv import load_dotenv, find_dotenv
import os
import pytest
import configparser
import imaplib


load_dotenv()
password = os.getenv("PASSWORD")
config = configparser.ConfigParser()
config.read("config.ini")
imap_server = config["DEFAULT"]["IMAP_SERVER"]
smtp_server = config["DEFAULT"]["SMTP_SERVER"]
email_address = config["DEFAULT"]["EMAIL_ADDRESS"]


def test_email():
    with EmailProxy(imap_server, email_address, password) as proxy:
        # check if the class has been constructed
        assert isinstance(proxy, EmailProxy)
        # check if we can fetch email from the mail server
        assert proxy.spin()

    # check if the connection got closed
    with pytest.raises(imaplib.IMAP4.error):
        proxy.imap.check()

    with SmtpConnection(smtp_server, email_address, password) as smtp_service:
        message = hm.make_email(email_address, email_address, "testing", "hello world")
        assert smtp_service.send_mail(message)
