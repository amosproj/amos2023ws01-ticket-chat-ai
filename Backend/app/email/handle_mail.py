import email
from email.message import Message
from email.header import decode_header
from bs4 import BeautifulSoup

from logger import logger


def can_be_processed(message):
    """
    should return false if the email was automatically generated or is from blocked user, will be implemented in later sprint
    :param message:
    :return boolean:
    """
    logger.info("Checking if email can be processed...")
    return True


def make_email(from_address, to_address, subject, message):
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
    msg["from"] = from_address
    msg["to"] = to_address
    msg["Subject"] = subject
    msg.set_content(message)
    return msg


def process(message: Message):
    sender = message.get("From")

    subject_e = decode_header(message.get("Subject"))
    subject = subject_e[0][0]
    if not type(subject) is str:
        subject = subject_e[0][0].decode(subject_e[0][1])
    content = ""
    attachments = []

    for part in message.walk():
        content_disposition = str(part.get("Content-Disposition"))
        if (
            part.get_content_type() == "text/plain"
            and "attachment" not in content_disposition
        ):
            charset = part.get_content_charset()
            content = part.get_payload(decode=True).decode(charset)
        elif (
            part.get_content_type() == "text/html"
            and "attachment" not in content_disposition
        ):
            charset = part.get_content_charset()
            soup = BeautifulSoup(part.get_payload(decode=True).decode(charset))
            content = soup.get_text()
        elif (
            part.get_content_maintype() in ["image", "application", "text"]
            and "attachment" in content_disposition
        ):
            filename = part.get_filename()
            if filename:
                attachments.append(
                    (
                        filename,
                        part.get_payload(decode=False),
                        part.get_content_type(),
                    )
                )

    content = content.replace("\xa0", "\n")
    content = content.replace("\r", "")
    return sender, subject, content.strip(), attachments
