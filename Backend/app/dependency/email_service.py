from fastapi.params import Depends
from app.email.smtp_conn import SmtpConnection
from app.service.email_service import EmailService
from app.dependency.smtp_connection import get_smtp_connection


def get_email_service(smtp_connection: SmtpConnection = Depends(get_smtp_connection)):
    return EmailService(smtp_connection)
