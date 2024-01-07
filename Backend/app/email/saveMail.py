# script to create test cases
import emailProxy as Proxy
import handle_mail as hm
import os
from dotenv import load_dotenv
import configparser
import email
import pickle


def save_mail():
    load_dotenv()
    password = os.getenv("PASSWORD")

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "..", "..", "config.ini"))
    imap_server = config["DEFAULT"]["IMAP_SERVER"]
    email_address = config["DEFAULT"]["EMAIL_ADDRESS"]
    smtp_server = config["DEFAULT"]["SMTP_SERVER"]
    try:
        with Proxy.EmailProxy(
            imap_server, smtp_server, email_address, password
        ) as proxy:
            msg_nums = proxy.spin()
            print("spun")
            for msgNum in msg_nums[0].split():
                _, data = proxy.imap.fetch(msgNum, "(RFC822)")

                message = email.message_from_bytes(data[0][1])
                print("received")

                with open(
                    os.path.join(
                        os.path.dirname(__file__), str(msgNum) + "_example.pkl"
                    ),
                    "wb",
                ) as outp:
                    pickle.dump(message, outp, pickle.HIGHEST_PROTOCOL)
                    print("dumped")
    except Exception as e:
        print(f"Error: {e}")


save_mail()
