from app.email.emailProxy import EmailProxy
from dotenv import load_dotenv
import os
import pytest

load_dotenv()

imap_server = os.getenv('IMAP_SERVER')
email_address = os.getenv('EMAIL_ADDRESS')
password = os.getenv('PASSWORD')

def test_email():
    #check, if .env file is set correctly in the test, if not copy the .env file from app/email into test/email
    assert imap_server=="outlook.office365.com"

    with EmailProxy(imap_server, email_address, password) as proxy:
        #check if the class has been constructed
        assert isinstance(proxy, EmailProxy)
        #check if we can fetch email from the mail server
        assert proxy.spin()

    #check if the connection got closed
    with pytest.raises(OSError):
        proxy.imap.socket().recv(10)
    
