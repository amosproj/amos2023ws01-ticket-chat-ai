import smtplib
import ssl
import time

from app.util.logger import logger


class SmtpConnection:
    smtp = None

    def __init__(self, smtp_server, email_address, email_password):
        self.smtp_server = smtp_server
        self.email_address = email_address
        self.email_password = email_password

    def __enter__(self):
        self.start_connection()
        return self

    def start_connection(self):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            self.smtp = smtplib.SMTP(self.smtp_server, 587)
            self.smtp.starttls(context=context)

            self.smtp.login(self.email_address, self.email_password)
            logger.info("SMTP connection established")
            return True
        except smtplib.SMTPConnectError as e:
            logger.exception(
                "Could not establish SMTP connection. Please restart the process."
            )
            raise Exception(
                "Could not establish SMTP connection. Please restart the process."
            )

    def try_reconnect(self):
        logger.warning("Lost connection to the SMTP server")
        logger.warning("Trying to reconnect SMTP in 5s")
        while True:
            try:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                self.smtp = smtplib.SMTP(self.smtp_server, 587)
                self.smtp.starttls(context=context)

                self.smtp.login(self.email_address, self.email_password)
                logger.info("SMTP reconnection successful")
                return True
            except:
                logger.warning("Trying to reconnect SMTP in 5s")
                time.sleep(5)

    def send_mail(self, message):
        try:
            self.smtp.send_message(message)
        except smtplib.SMTPServerDisconnected as e:
            logger.exception(f"SMTP error: {e}")
            self.try_reconnect()
            self.send_mail(message)

        return True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.smtp.quit()
        logger.info("SMTP connection closed")
        return True
