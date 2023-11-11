import imaplib
import email
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

imap_server = os.getenv('IMAP_SERVER')
email_address = os.getenv('EMAIL_ADDRESS')
password = os.getenv('PASSWORD')

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_address, password) #TODO: Change gmail settings to allow less secure apps to access email account

imap.select("Inbox")

_, msgNums = imap.search(None, "ALL")

for msgNum in msgNums[0].split():
    _, data = imap.fetch(msgNum, "(RFC822)")

    message = email.message_from_bytes(data[0][1])

    print(f"Message Number: {msgNum}")
    print(f"From: {message.get('From')}")
    print(f"To: {message.get('To')}")
    print(f"BCC: {message.get('BCC')}")
    print(f"Date: {message.get('Date')}")
    print(f"Subject: {message.get('Subject')}")

    print("Content:")
    for part in message.walk():
        if part.get_content_type() == "text/plain":
            print(part.as_string())

imap.close()