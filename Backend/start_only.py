import os
import sys
import subprocess
import signal
import time
import webbrowser


def start_server():
    # mac os, need to be tested
    if sys.platform == "darwin":
        os.system("brew services start mongodb-community@7.0")
    # windows, if the standard installation is not changed
    elif sys.platform == "win32":
        os.system(
            'start /B cmd /k "C:\\Program Files\\MongoDB\\Server\\7.0\\bin\\mongod.exe"'
        )
    # linux, need to be testest
    elif sys.platform == "linux":
        return os.system("sudo systemctl start mongod")


def stop_server():
    # mac os
    if sys.platform == "darwin":
        os.system("brew services stop mongodb-community@7.0")
    # windows
    elif sys.platform == "win32":
        os.system("taskkill /IM mongod.exe /F")
    # linux
    elif sys.platform == "linux":
        return os.system("sudo systemctl stop mongod")


def start_backend():
    subprocess.Popen(["uvicorn", "app.main:app", "--reload"], cwd="Backend")


def start_frontend():
    subprocess.Popen(["npm.cmd", "start"], cwd="Frontend")
    time.sleep(5)
    webbrowser.open("http://localhost:4200/")


def start_email_proxy():
    subprocess.Popen(["python", "main.py"], cwd="Backend/app/email")


def exit_handler():
    print("Script wird beendet. Stoppe MongoDB...")
    stop_server()


def main():
    start_server()
    start_backend()
    start_frontend()
    start_email_proxy()


if __name__ == "__main__":
    # register proxy exit
    signal.signal(signal.SIGINT, exit_handler)

    main()
