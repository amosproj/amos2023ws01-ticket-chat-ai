import imaplib
import email
import os
from dotenv import load_dotenv
import sched, time
scheduler = sched.scheduler(time.monotonic, time.sleep)


def receive_unseen_emails():
    load_dotenv(dotenv_path='.env')

    imap_server = os.getenv('IMAP_SERVER')
    email_address = os.getenv('EMAIL_ADDRESS')
    password = os.getenv('PASSWORD')

    imap = imaplib.IMAP4_SSL(imap_server, port=993)
    imap.login(email_address, password)

    imap.select("Inbox")

    _, msgNums = imap.search(None, "UNSEEN")

    for msgNum in msgNums[0].split():
        _, data = imap.fetch(msgNum, "(RFC822)")

        message = email.message_from_bytes(data[0][1])

        print(f"Message Number: {msgNum}")
        print(f"From: {message.get('From')}")
        print(f"Subject: {message.get('Subject')}")

        print("Content:")
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                print(part.as_string())

    imap.close()


def scheduler_method():
    print("Tick")
    receive_unseen_emails()


scheduler.enter(5, 1, scheduler_method, ())
scheduler.enter(5, 1, scheduler_method, ())
scheduler.run()

