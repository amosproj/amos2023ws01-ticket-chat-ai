import email
from email.message import Message
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup


def can_be_processed(message, blacklisted_emails, logger):
    """
    Returns False if the email is in the blacklist.
    :param message: Email message object
    :param blacklisted_emails: list of email addresses
    :param logger: logger
    :return: bool
    """
    logger.info("Checking if email can be processed...")

    # Extract sender's email address
    sender = message.get("From", "")

    # Check if the sender is in the blacklist
    if any(blacklisted_email in sender for blacklisted_email in blacklisted_emails):
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
    msg = email.message.EmailMessage()
    msg["from"] = from_address
    msg["to"] = to_address
    msg["Subject"] = subject
    msg.set_content(message)
    return msg


def make_email_with_html(from_address, to_address, ticket, logger):
    """
    creates email type with an html part
    :param from_address:
    :param to_address:
    :param ticket: ticket object as defined in app/api/dto/ticket.py or dictionary
    :param logger: logger
    :return email:
    """

    if isinstance(ticket, dict):
        ticket_id = ticket["id"]
        ticket_title = ticket["title"]
        ticket_service = ticket["service"]
        ticket_category = ticket["category"]
        ticket_keywords = ticket["keywords"]
        ticket_customerPriority = ticket["customerPriority"]
        ticket_affectedPerson = ticket["affectedPerson"]
        ticket_description = ticket["description"]
        ticket_priority = ticket["priority"]
        ticket_attachmentNames = ticket["attachmentNames"]
        ticket_requestType = ticket["requestType"]
    else:
        ticket_id = ticket.id
        ticket_title = ticket.title
        ticket_service = ticket.service
        ticket_category = ticket.category
        ticket_keywords = ticket.keywords
        ticket_customerPriority = ticket.customerPriority
        ticket_affectedPerson = ticket.affectedPerson
        ticket_description = ticket.description
        ticket_priority = ticket.priority
        ticket_attachmentNames = ticket.attachmentNames
        ticket_requestType = ticket.requestType

    logger.info("Creating html message...")
    msg = MIMEMultipart("alternative")
    msg["from"] = from_address
    msg["to"] = to_address
    subject = "Support ticket created: " + ticket_title
    msg["Subject"] = subject

    html_head = (
        '<head><style type="text/css">'
        ".tg  {border-collapse:collapse;border-spacing:0;}"
        ".tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;"
        "overflow:hidden;padding:10px 5px;word-break:normal;}"
        ".tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;"
        "font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}"
        ".tg .tg-1wig{font-weight:bold;text-align:left;vertical-align:top}"
        ".tg .tg-0lax{text-align:left;vertical-align:top}</style></head>"
    )

    table_elements = [
        ("ID:", ticket_id),
        ("Title:", ticket_title),
        ("Service:", ticket_service or ""),
        ("Category:", ticket_category or ""),
        ("Keywords:", str(ticket_keywords or "")),
        ("Customer priority:", ticket_customerPriority or ""),
        ("Affected Person:", ticket_affectedPerson or ""),
        ("Description:", ticket_description),
        ("Priority:", ticket_priority or ""),
        ("Attachments:", str(ticket_attachmentNames or "")),
        ("Request type:", ticket_requestType or ""),
    ]

    table = '<table class="tg">'
    for i in table_elements:
        table += (
            '<tr><td class="tg-1wig">'
            + i[0]
            + '</td><td class="tg-0lax">'
            + i[1]
            + "</td></tr>"
        )
    table += "</table><br>"

    salutation = "Hi there!<br><br>your ticket has been created successfully. Please find below the respective details:"
    ending = "Cheers,<br>TalkTix"

    text = (
        "Hi there!\n\nyour ticket has been created successfully. Your ticket number is:"
        + ticket_id
        + ".\n\nCheers,\nTalkTix"
    )
    html = (
        "<html>" + html_head + "<body>" + salutation + table + ending + "</body></html>"
    )

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)

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
