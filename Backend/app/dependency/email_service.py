from fastapi.params import Depends
from app.dependency.smtp_connection import get_smtp_connection
from app.email_router.email_service import EmailService

from app.email_router.smtp_conn import SmtpConnection



def get_email_service(smtp_connection: SmtpConnection = Depends(get_smtp_connection)):
    return EmailService(smtp_connection)
