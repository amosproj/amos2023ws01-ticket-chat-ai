import email
from fastapi import Depends
from app.email.smtp_conn import SmtpConnection
from app.email.handle_mail import make_email_with_html
from app.dependency.smtp_connection import get_smtp_connection
from app.util.logger import logger


class EmailService:
    def __init__(self, smtp_conn: SmtpConnection) -> None:
        self.smtp_conn = smtp_conn
        self.smtp_conn.start_connection()
        self.email_address = smtp_conn.email_address

    def send_email(self, sender, ticket_dict):
        msg = make_email_with_html(self.email_address, sender, ticket_dict, logger)
        self.smtp_conn.send_mail(msg)
