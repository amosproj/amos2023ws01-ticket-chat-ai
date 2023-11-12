import os
import sys


def start_server() -> int:
    # mac os
    if sys.platform == "darwin":
        return os.system("brew services start mongodb-community@7.0")
    # windows
    elif sys.platform == "win32":
        return os.system("elevate -w net start MongoDB")
    # linux
    elif sys.platform == "linux":
        return os.system("sudo systemctl start mongod")


def stop_server() -> int:
    # mac os
    if sys.platform == "darwin":
        return os.system("brew services stop mongodb-community@7.0")
    # windows
    elif sys.platform == "win32":
        return os.system("elevate -w net stop MongoDB")
    # linux
    elif sys.platform == "linux":
        return os.system("sudo systemctl stop mongod")
