import email


def can_be_processed(message):
    """
    should return false if the email was automatically generated or is from blocked user, will be implemented in later sprint
    :param message:
    :return boolean:
    """
    return True


def make_email(from_address, to_address, subject, message):
    msg = email.message.EmailMessage()
    msg["from"] = from_address
    msg["to"] = to_address
    msg["Subject"] = subject
    msg.set_content(message)
    return msg
