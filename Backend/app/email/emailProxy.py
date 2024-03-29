import email
import imaplib
import time

import handle_mail as hm
import smtp_conn as sm
from logger import logger


class EmailProxy:
    imap = None
    smtp = None

    def __init__(
        self,
        imap_server,
        smtp_server,
        email_address,
        email_password,
        blacklisted_emails,
    ):
        self.imap_server = imap_server
        self.email_address = email_address
        self.email_password = email_password
        self.smtp_server = smtp_server
        self.blacklisted_emails = blacklisted_emails

    def __enter__(self):
        self.start_connection()
        self.smtp = sm.SmtpConnection(
            self.smtp_server, self.email_address, self.email_password, logger
        )
        self.smtp.start_connection()
        return self

    def start_connection(self):
        """
        connects to the imap server
        :return:
        """
        try:
            self.imap = imaplib.IMAP4_SSL(self.imap_server, port=993)
            self.imap.login(self.email_address, self.email_password)

            self.imap.select("Inbox")
            logger.info("IMAP connection established")
            return True

        except imaplib.IMAP4.abort as e:
            logger.exception(
                "Could not establish IMAP connection. Pls restart process."
            )
            raise Exception("Could not establish IMAP connection. Pls restart process.")

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
        """
        searches for new messages
        :return: List of message numbers.
        """
        try:
            _, msg_nums = self.imap.search(None, "UNSEEN")
            print("msg_nums: " + str(msg_nums))

        except imaplib.IMAP4.abort as e:
            logger.exception(f"IMAP error: {e}")
            self.try_reconnect()
            msg_nums = self.spin()

        return msg_nums

    def process_mail(self, msgNum):
        """
        Fetches Email and processes it.
        :param msgNum: The number of the message to be processed.
        :return: Tuple with sender, subject, and content of the message
        """
        try:
            _, data = self.imap.fetch(msgNum, "(RFC822)")

            message = email.message_from_bytes(data[0][1])
            if hm.can_be_processed(message, self.blacklisted_emails, logger):
                # specific processing
                return hm.process(message)
            else:
                return None, None, None, None
        except imaplib.IMAP4.abort:
            self.try_reconnect()
            return self.process_mail(self, msgNum)
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        close the connection to the imap server
        :param exc_type: exception_type
        :param exc_val: exception_value
        :param exc_tb: traceback
        :return:
        """
        if exc_type:
            if exc_type != KeyboardInterrupt:
                logger.error("Error: ", exc_info=(exc_type, exc_val, exc_tb))
            else:
                logger.info("Keyboard Interrupt, Application is shutting down")
        self.imap.close()
        self.imap.logout()
        self.smtp.smtp.quit()
        logger.info("Connection closed")
        return True
