import os
import pickle
import sys
from unittest import TestCase

# determine the absolute path to the 'backend' directory
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# add the directory 'backend/app/email/' to sys.path
sys.path.append(os.path.join(backend_path, "app", "email"))

from app.email.handle_mail import process


class HandleMailTest(TestCase):
    def test_process_with_mail_no_attachment(self):
        file_path = os.path.join(
            os.path.dirname(__file__), "test_mails/b'263'_no_attachment.pkl"
        )
        with open(file_path, "rb") as inp:
            message = pickle.load(inp)
            # Act
            sender, subject, content, attachments = process(message)
            # Expect
            self.assertEqual("Dies ist ein Test ohne Anhang", content)
            self.assertEqual('"Fabian Weber" <webef98@zedat.fu-berlin.de>', sender)
            self.assertEqual("test ohne anhang", subject)
            self.assertFalse(not content)

    def test_process_with_mail_with_one_attachment(self):
        file_path = os.path.join(
            os.path.dirname(__file__), "test_mails/b'264'_example_png.pkl"
        )
        with open(file_path, "rb") as inp:
            message = pickle.load(inp)
            # Act
            sender, subject, content, attachments = process(message)
            # Expect
            self.assertEqual('"Fabian Weber" <webef98@zedat.fu-berlin.de>', sender)
            self.assertEqual("test mit png", subject)
            self.assertFalse(not content)
            self.assertEqual(1, len(attachments))

    def test_process_with_mail_with_multiple_attachments(self):
        file_path = os.path.join(
            os.path.dirname(__file__), "test_mails/b'265'_multiple_attachments.pkl"
        )
        with open(file_path, "rb") as inp:
            message = pickle.load(inp)
            # Act
            sender, subject, content, attachments = process(message)
            # Expect
            self.assertEqual('"Fabian Weber" <webef98@zedat.fu-berlin.de>', sender)
            self.assertEqual("Test mit mehreren Anhängen", subject)
            self.assertFalse(not content)
            self.assertEqual(2, len(attachments))

    def test_process_with_mail_with_text_plain_MIMEtype_attachment(self):
        file_path = os.path.join(
            os.path.dirname(__file__), "test_mails/b'366'_text_plain_attachment.pkl"
        )
        with open(file_path, "rb") as inp:
            message = pickle.load(inp)
            # Act
            sender, subject, content, attachments = process(message)
            # Expect
            self.assertEqual("Garvin Konopka <konopkagarvin@gmail.com>", sender)
            self.assertEqual("TestMail mit .txt Attachment", subject)
            self.assertEqual("Hallo,\n\ndas ist ein Test-Mailinhalt.", content)
            self.assertEqual(1, len(attachments))

    def test_process_with_html(self):
        file_path = os.path.join(
            os.path.dirname(__file__), "test_mails/b'367'_tumail.pkl"
        )
        with open(file_path, "rb") as inp:
            message = pickle.load(inp)
            # Act
            sender, subject, content, attachments = process(message)
            # Expect
            self.assertEqual("Hallo,\nDas ist ein Test.\nBye", content)

    def test_process_with_special_chars(self):
        file_path = os.path.join(
            os.path.dirname(__file__), "test_mails/b'368'_sonderzeichen.pkl"
        )
        with open(file_path, "rb") as inp:
            message = pickle.load(inp)
            # Act
            sender, subject, content, attachments = process(message)
            # Expect
            self.assertEqual("Encoding Test", subject)
            self.assertEqual("Hällochen,\nöüßä\nBye", content)

    def test_process_with_special_chars2(self):
        file_path = os.path.join(
            os.path.dirname(__file__), "test_mails/b'369'_sonderzeichen2.pkl"
        )
        with open(file_path, "rb") as inp:
            message = pickle.load(inp)
            # Act
            sender, subject, content, attachments = process(message)
            # Expect
            self.assertEqual("Special chars", subject)
            self.assertEqual("Ä\nÖ\nÜ", content)

    def test_process_with_special_subject(self):
        file_path = os.path.join(
            os.path.dirname(__file__), "test_mails/b'370'_special_char_subject.pkl"
        )
        with open(file_path, "rb") as inp:
            message = pickle.load(inp)
            # Act
            sender, subject, content, attachments = process(message)
            # Expect
            self.assertEqual("Sönderzächenüß", subject)

    def test_process_web_de_app(self):
        file_path = os.path.join(
            os.path.dirname(__file__), "test_mails/b'371'_web_de_app.pkl"
        )
        with open(file_path, "rb") as inp:
            message = pickle.load(inp)
            # Act
            sender, subject, content, attachments = process(message)
            # Expect
            self.assertEqual("Test web de mail", subject)
            self.assertEqual(
                "Dies ist ein test. --Diese Nachricht wurde von meinem Android Mobiltelefon "
                "mit WEB.DE Mail gesendet.", content
            )

    def test_process_gmail_app_apple(self):
        file_path = os.path.join(
            os.path.dirname(__file__), "test_mails/b'372'_gmail_app_apple.pkl"
        )
        with open(file_path, "rb") as inp:
            message = pickle.load(inp)
            # Act
            sender, subject, content, attachments = process(message)
            # Expect
            self.assertEqual("Test", subject)
            self.assertEqual("Test from apple mail\nSent from my iPhone", content)

    def test_process_forwarding(self):
        file_path = os.path.join(
            os.path.dirname(__file__), "test_mails/b'373'_forwarded.pkl"
        )
        with open(file_path, "rb") as inp:
            message = pickle.load(inp)
            # Act
            sender, subject, content, attachments = process(message)
            # Expect
            self.assertEqual("Fwd: Weiterleiten Täst", subject)
            self.assertEqual(
                "---------- Forwarded message ---------From: irild hoxhallari "
                "<ihoxhallari@gmail.com>Date: Sat, 16 Dec 2023 at 12:57Subject: Weiterleiten TästTo:  "
                "<irhox100@gmail.com>Hallo,\ndas ist ein Test,\nGrüße", content
            )
