import configparser
import os

from dotenv import load_dotenv
from app.email_router.smtp_conn import SmtpConnection


def get_smtp_connection():
    load_dotenv()
    password = os.getenv("PASSWORD")

    config = configparser.ConfigParser()
    config.read("config.ini")
    smtp_server = config["DEFAULT"]["SMTP_SERVER"]
    email_address = config["DEFAULT"]["EMAIL_ADDRESS"]

    return SmtpConnection(smtp_server, email_address, password)
