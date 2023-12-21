import os
import sys
import subprocess


def install_backend_dependencies():
    subprocess.run(["pip", "install", "-r", "requirements.txt"], cwd="Backend")


def install_frontend_dependencies():
    subprocess.Popen(["npm.cmd", "install", "-g", "n"], cwd="Frontend")
    subprocess.Popen(["npm.cmd", "install", "-g", "@angular/cli"], cwd="Frontend")
    subprocess.Popen(["npm.cmd", "install"], cwd="Frontend")


def main():
    install_backend_dependencies()
    install_frontend_dependencies()

    print("All requirements has been initialized.")


if __name__ == "__main__":
    main()
