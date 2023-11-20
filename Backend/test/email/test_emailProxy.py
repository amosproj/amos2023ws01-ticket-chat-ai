from app.email.emailProxy import EmailProxy
from app.email.smtp_conn import SmtpConnection
import app.email.handle_mail as hm
from dotenv import load_dotenv, find_dotenv
import os
import pytest
import configparser
import imaplib
import time


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
            email_address, email_address,  test_subject, test_content
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
