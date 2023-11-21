from app.persistence.ticket_db_service import TicketDBService
import app.email.emailProxy as Proxy
import app.email.handle_mail as hm
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

    with Proxy.EmailProxy(imap_server, smtp_server, email_address, password) as proxy:
        while True:
            time.sleep(sleep_timer)
            msg_nums = proxy.spin()
            for msgNum in msg_nums[0].split():
                (sender, subject, content) = proxy.process_mail(msgNum)

                # send message to backend
                email = "Von: " + sender + "\nBetreff: " + subject + "\n" + content
                received_dict = trained_t5_model.run_model(email)
                print(email)
                print(received_dict)

                # Save the ticket to the database using the TicketDBService
                ticket_db_service = TicketDBService()
                ticket_db_service.save_ticket(received_dict)

                # send response
                new_email = hm.make_email(
                    email_address, sender, "RE:" + subject, received_dict
                )
                proxy.smtp.send_mail(new_email)
