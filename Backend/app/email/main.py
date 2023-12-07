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
    config.read("../../config.ini")
    imap_server = config["DEFAULT"]["IMAP_SERVER"]
    smtp_server = config["DEFAULT"]["SMTP_SERVER"]
    email_address = config["DEFAULT"]["EMAIL_ADDRESS"]
    sleep_timer = int(config["DEFAULT"]["SLEEP_TIMER"])

    try:
        with Proxy.EmailProxy(
            imap_server, smtp_server, email_address, password
        ) as proxy:
            while True:
                # tmp_dir = "./tmp"
                # os.makedirs(tmp_dir, exist_ok=True)
                msg_nums = proxy.spin()
                for msgNum in msg_nums[0].split():
                    (sender, subject, content, attachments) = proxy.process_mail(msgNum)
                    print(sender)
                    print(subject)
                    print(content)
                    print(attachments)

                    # send message to backend
                    email = f"Von: {sender}\nBetreff: {subject}\n {content}"
                    json_input = {"text": email}
                    if content != "":
                        response = requests.post(
                            "http://localhost:8000/api/v1/ticket/text",
                            data=json.dumps(json_input),
                        )
                        ticket = json.loads(response.text)
                        logger.info("Received ticket: " + ticket["id"])
                        time.sleep(10)
                        if attachments:
                            files = {f"file{i}": (file_path, open(file_path, 'rb'), "image/png") for i, file_path in enumerate(attachments)}
                            print("BEFORE: ", files)
                            attachments_response = requests.put(
                                "http://localhost:8000/api/v1/ticket/" + ticket["id"] + "/attachments",
                                files=files,
                            )
                            print("attach: ", attachments_response)
                            logger.info("Attachments for ticket: " + ticket["id"] + " are sent to the API")

                        # send response
                        new_email = hm.make_email(
                            email_address, sender, "RE:" + subject, response.text
                        )
                        proxy.smtp.send_mail(new_email)
                time.sleep(sleep_timer)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run_proxy()
