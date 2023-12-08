import email
from fastapi import Depends

from app.dependency.smtp_connection import get_smtp_connection
from app.email_router.smtp_conn import SmtpConnection
from app.util.logger import logger


class EmailService:
    def __init__(
        self, smtp_conn: SmtpConnection = Depends(get_smtp_connection)
    ) -> None:
        self.smtp_conn = smtp_conn
        self.smtp_conn.start_connection()
        self.email_address = smtp_conn.email_address

    def send_email(self, sender, subject, content):
        msg = self.make_email(sender, subject, content)
        self.smtp_conn.send_mail(msg)

    def make_email(self, to_address, subject, message):
        """
        creates email type with specified data
        :param from_address:
        :param to_address:
        :param subject:
        :param message:
        :return email:
        """
        logger.info("Creating email message...")
        msg = email.message.EmailMessage()
        msg["from"] = self.email_address
        msg["to"] = to_address
        msg["Subject"] = subject
        msg.set_content(message)
        return msg
