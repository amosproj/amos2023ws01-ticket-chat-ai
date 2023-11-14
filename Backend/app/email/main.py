import emailProxy as Proxy
import os
from dotenv import load_dotenv
import time
import configparser


def run_proxy():
    load_dotenv()
    password = os.getenv("PASSWORD")

    config = configparser.ConfigParser()
    config.read("config.ini")
    imap_server = config["DEFAULT"]["IMAP_SERVER"]
    email_address = config["DEFAULT"]["EMAIL_ADDRESS"]
    sleep_timer = int(config["DEFAULT"]["SLEEP_TIMER"])

    with Proxy.EmailProxy(imap_server, email_address, password) as proxy:
        while True:
            time.sleep(sleep_timer)
            proxy.spin()


if __name__ == "__main__":
    run_proxy()
