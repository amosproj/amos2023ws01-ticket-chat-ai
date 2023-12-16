import email
from email.message import Message
from email.header import decode_header
from bs4 import BeautifulSoup

from logger import logger


def replace_special_chars(text):
    text = text.replace("=E4", "ä")
    text = text.replace("=F6", "ö")
    text = text.replace("=FC", "ü")
    text = text.replace("=DF", "ß")
    text = text.replace("=C4", "Ä")
    text = text.replace("=D6", "Ö")
    text = text.replace("=DC", "Ü")

    text = text.replace("=C3=A4", "ä")
    text = text.replace("=C3=B6", "ö")
    text = text.replace("=C3=BC", "ü")
    text = text.replace("=C3=9F", "ß")
    text = text.replace("=C3=84", "Ä")
    text = text.replace("=C3=96", "Ö")
    text = text.replace("=C3=9C", "Ü")

    text = text.replace("\xa0", "\n")
    text = text.replace("=\n", "")
    return text

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
            content = part.as_string()
        elif (
            part.get_content_type() == "text/html"
            and "attachment" not in content_disposition
        ):
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

    # clean up the content string
    content = content.split("MIME-Version: 1.0")[-1].strip().split("\n")
    real_content = ""
    for line in content:
        line_ok = True
        if "Content-Type:" in line:
            line_ok = False
        if "Message-Part" in line:
            line_ok = False
        if "Content-Transfer-Encoding:" in line:
            line_ok = False
        if line_ok:
            real_content += line + "\n"

    real_content = replace_special_chars(real_content)

    return sender, subject, real_content.strip(), attachments
