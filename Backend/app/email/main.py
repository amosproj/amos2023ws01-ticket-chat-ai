import emailProxy as Proxy
import os
from dotenv import load_dotenv
import sched, time


def run_proxy():
    load_dotenv()

    imap_server = os.getenv('IMAP_SERVER')
    email_address = os.getenv('EMAIL_ADDRESS')
    password = os.getenv('PASSWORD')
    print(imap_server)
    with Proxy.EmailProxy(imap_server, email_address, password) as proxy:
        while True:
            time.sleep(60)
            proxy.spin()


if __name__ == '__main__':
    run_proxy()
