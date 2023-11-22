import imaplib
import time
import email
import handle_mail as hm
import smtp_conn as sm
from app.logger import logger  # Import your logger

class EmailProxy:
    imap = None
    smtp = None

    def __init__(self, imap_server, smtp_server, email_address, email_password):
        self.imap_server = imap_server
        self.email_address = email_address
        self.email_password = email_password
        self.smtp_server = smtp_server

    def __enter__(self):
        self.start_connection()
        self.smtp = sm.SmtpConnection(
            self.smtp_server, self.email_address, self.email_password
        )
        self.smtp.start_connection()
        return self

    def start_connection(self):
        try:
            self.imap = imaplib.IMAP4_SSL(self.imap_server, port=993)
            self.imap.login(self.email_address, self.email_password)

            self.imap.select("Inbox")
            logger.info("IMAP connection established")
            return True

        except imaplib.IMAP4.abort as e:
            logger.exception("Could not establish IMAP connection. Please restart the process.")
            raise Exception("Could not establish IMAP connection. Please restart the process.")

    def try_reconnect(self):
        logger.warning("Lost connection to the IMAP server")
        logger.warning("Trying to reconnect IMAP in 5s")
        while True:
            try:
                self.imap = imaplib.IMAP4_SSL(self.imap_server, port=993)
                self.imap.login(self.email_address, self.email_password)
                self.imap.select("Inbox")
                logger.info("IMAP reconnection successful")
                return True
            except:
                logger.warning("Trying to reconnect IMAP in 5s")
                time.sleep(5)

    def spin(self):
        try:
            _, msg_nums = self.imap.search(None, "UNSEEN")

        except imaplib.IMAP4.abort as e:
            logger.error(f"IMAP error: {e}")
            self.try_reconnect()
            msg_nums = self.spin()

        return msg_nums

    def process_mail(self, msgNum):
        try:
            _, data = self.imap.fetch(msgNum, "(RFC822)")

            message = email.message_from_bytes(data[0][1])
            # specific processing
            sender = message.get("From")
            subject = message.get("Subject")
            content = ""

            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    content += part.as_string()
                    content += "\n"
            return (sender, subject, content)
        except:
            logger.exception("Error while processing mail. Attempting reconnection.")
            self.try_reconnect()
            return self.process_mail(self, msgNum)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.imap.close()
        self.imap.logout()
        self.smtp.smtp.quit()
        logger.info("Connection closed")
        return True
