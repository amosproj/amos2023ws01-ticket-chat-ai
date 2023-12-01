import json

import emailProxy as Proxy
import handle_mail as hm
import os
from dotenv import load_dotenv
import time
import configparser
import requests


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
                msg_nums = proxy.spin()
                for msgNum in msg_nums[0].split():
                    (sender, subject, content) = proxy.process_mail(msgNum)

                    # send message to backend
                    email = f'"text":"Von: {sender}\nBetreff: {subject}\n {content}"'
                    json_input = {"text": email}
                    print(json_input)
                    if content != "":
                        response = requests.post(
                            "http://localhost:8000/api/v1/ticket/text",
                            data=json.dumps(json_input),
                        )
                        print(response.text)

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
