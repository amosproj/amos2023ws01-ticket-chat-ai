import app.email.emailProxy as Proxy
import os
from dotenv import load_dotenv
import time
import configparser
from app.model.t5.use_trained_t5_model import TrainedT5Model

def run_proxy():
    load_dotenv()
    password = os.getenv("PASSWORD")

    config = configparser.ConfigParser()
    config.read("./config.ini")
    imap_server = config["DEFAULT"]["IMAP_SERVER"]
    smtp_server = config["DEFAULT"]["SMTP_SERVER"]
    email_address = config["DEFAULT"]["EMAIL_ADDRESS"]
    sleep_timer = int(config["DEFAULT"]["SLEEP_TIMER"])
    trained_t5_model = TrainedT5Model()

    with Proxy.EmailProxy(imap_server, email_address, password) as proxy:
        while True:
            time.sleep(sleep_timer)
            new_emails = proxy.spin()
            emails_list = new_emails.split("Message Number:")
            for email in emails_list:
                if email != "":
                    received_text = trained_t5_model.run_model(email)
                    print(email)
                    print(received_text)
