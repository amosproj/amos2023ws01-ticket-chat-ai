import email
from email.message import Message
from email.header import decode_header
from bs4 import BeautifulSoup

from logger import logger

# Define a list of email addresses or domains to be ignored
BLACKLIST = ["xyz@microsoft.com"]


def can_be_processed(message):
    """
    Returns False if the email is in the blacklist.
    :param message: Email message object
    :return: bool
    """
    logger.info("Checking if email can be processed...")

    # Extract sender's email address
    sender = message.get("From", "").lower()

    # Check if the sender is in the blacklist
    if any(blacklisted_email in sender for blacklisted_email in BLACKLIST):
        logger.warning(f"Ignoring email from the blacklist: {sender}")
        return False

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

            # if charset is none we fallback to default UTF-8,
            # if it fails because of an unknown different charset we fallback to part.as_string()
            if charset:
                content = part.get_payload(decode=True).decode(charset)
            else:
                try:
                    content = part.get_payload(decode=True).decode()
                except UnicodeDecodeError:
                    content = part.as_string()
        elif (
            part.get_content_type() == "text/html"
            and "attachment" not in content_disposition
        ):
            charset = part.get_content_charset()
            if charset:
                soup = BeautifulSoup(part.get_payload(decode=True).decode(charset))
            else:
                try:
                    soup = BeautifulSoup(part.get_payload(decode=True).decode())
                except UnicodeDecodeError:
                    soup = BeautifulSoup(part.as_string())
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
