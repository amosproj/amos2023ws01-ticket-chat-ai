import imaplib
import email
import app.email.handle_mail as hm
import app.email.smtp_conn as sm


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
        """
        connects to the imap server
        :return:
        """
        self.imap = imaplib.IMAP4_SSL(self.imap_server, port=993)
        self.imap.login(self.email_address, self.email_password)

        self.imap.select("Inbox")
        print("connection established")
        return True

    def spin(self):
        """
        searches for new messages
        :return: List of message numbers.
        """
        _, msg_nums = self.imap.search(None, "UNSEEN")
        return msg_nums

    def process_mail(self, msgNum):
        """
        Fetches Email and processes it.
        :param msgNum: The number of the message to be processed.
        :return: Tuple with sender, subject, and content of the message
        """
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

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        close the connection to the imap server
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.imap.close()
        self.imap.logout()
        self.smtp.smtp.quit()
        print("connection closed")
        return True
