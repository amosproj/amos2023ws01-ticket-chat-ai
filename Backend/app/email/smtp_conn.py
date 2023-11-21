import smtplib
import ssl


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
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        self.smtp = smtplib.SMTP(self.smtp_server, 587)
        self.smtp.starttls(context=context)

        self.smtp.login(self.email_address, self.email_password)
        return True

    def send_mail(self, message):
        self.smtp.send_message(message)
        return True

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        close the connection to the imap server
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.smtp.quit()
        print("SMTP connection closed")
        return True
