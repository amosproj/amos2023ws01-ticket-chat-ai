import email

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


def process(message):
    sender = message.get("From")
    subject = message.get("Subject")
    content = ""
    attachments = []

    for part in message.walk():
        if part.get_content_type() == "text/plain":
            content += part.as_string()
            content += "\n"
        # Check if the content type is multipart
        if part.get_content_maintype() == "multipart":
            continue
        # Check if there's an attachment
        if part.get("Content-Disposition") is None:
            continue
        filename = part.get_filename()
        if filename:
            attachments.append(
                (
                    filename,
                    part.get_payload(decode=False),
                    part.get_content_type(),
                )
            )
    return sender, subject, content, attachments
