import imaplib
import email

class EmailProxy:
    imap = None

    def __init__(self, imap_server, email_address, email_password):
        self.imap_server = imap_server
        self.email_address = email_address
        self.email_password = email_password

    def __enter__(self):
        self.start_connection()
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
        fetches emails, calls process_mail if email can be processed
        :return:
        """
        _, msgNums = self.imap.search(None, "UNSEEN")

        for msgNum in msgNums[0].split():
            _, data = self.imap.fetch(msgNum, "(RFC822)")

            message = email.message_from_bytes(data[0][1])

            if self.can_be_processed(message):
                print(f"Message Number: {msgNum}")
                self.process_mail(message)
        return True

    def can_be_processed(self, email):
        """
        should return false if the email was automatically generated or is from blocked user, will be implemented in later sprint
        :param email:
        :return boolean:
        """
        return True

    def process_mail(self, message):
        """
        communicates with backend, answers to email, for now it just prints the content of the email
        :param email:
        :return:
        """
        print(f"From: {message.get('From')}")
        print(f"Subject: {message.get('Subject')}")

        print("Content:")
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                print(part.as_string())
        return True

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
        print("connection closed")
        return True
