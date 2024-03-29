import json

import emailProxy as Proxy
import handle_mail as hm
import os
from dotenv import load_dotenv
import time
import configparser
import requests
from logger import logger


def run_proxy():
    load_dotenv()
    password = os.getenv("PASSWORD")

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "..", "..", "config.ini"))
    imap_server = config["DEFAULT"]["IMAP_SERVER"]
    smtp_server = config["DEFAULT"]["SMTP_SERVER"]
    email_address = config["DEFAULT"]["EMAIL_ADDRESS"]
    sleep_timer = int(config["DEFAULT"]["SLEEP_TIMER"])
    blacklisted_emails = list(
        filter(
            None, [e.strip() for e in config.get("DEFAULT", "BLACKLIST").split("\n")]
        )
    )

    try:
        with Proxy.EmailProxy(
            imap_server, smtp_server, email_address, password, blacklisted_emails
        ) as proxy:
            while True:
                msg_nums = proxy.spin()
                for msgNum in msg_nums[0].split():
                    (sender, subject, content, attachments) = proxy.process_mail(msgNum)
                    if sender is None:
                        continue
                    else:
                        # send message to backend
                        json_input = {
                            "text": f"Subject: {subject}\n Content: {content}",
                            "email": sender,
                        }
                        success = True

                        if content != "":
                            try:
                                response = requests.post(
                                    "http://localhost:8000/api/v1/ticket/text",
                                    data=json.dumps(json_input),
                                )
                                if attachments:
                                    response = requests.put(
                                        "http://localhost:8000/api/v1/ticket/"
                                        + ticket["id"]
                                        + "/attachments",
                                        files=[
                                            ("files", attachment)
                                            for attachment in attachments
                                        ],
                                    )
                                    logger.info(
                                        "Attachments for ticket: "
                                        + ticket["id"]
                                        + " are sent to the API"
                                    )
                                ticket = json.loads(response.text)
                                logger.info("Received ticket: " + ticket["id"])
                            except Exception as e:
                                logger.error(
                                    f"Didn't receive the ticket from backend: {e}"
                                )
                                success = False

                            if success:
                                new_email = hm.make_email_with_html(
                                    email_address, sender, ticket, logger
                                )
                            else:
                                new_email = hm.make_email(
                                    email_address,
                                    sender,
                                    "Ticket could not be created",
                                    "Hello,\nunfortunately your support ticket couldnt be created, try it out later again.",
                                )

                            logger.info("Sending the email")
                            proxy.smtp.send_mail(new_email)
                time.sleep(sleep_timer)

    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    run_proxy()
