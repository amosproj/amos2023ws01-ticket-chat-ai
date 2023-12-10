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
            self.assertEqual("=?utf-8?B?VGVzdCBtaXQgbWVocmVyZW4gQW5ow6RuZ2Vu?=", subject)
            self.assertFalse(not content)
            self.assertEqual(2, len(attachments))
