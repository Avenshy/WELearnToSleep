import os

NAME = "WELearnToSleep"
VERSION = "0.4.0"

os.system(f"pyinstaller -F --name {NAME}.{VERSION} ./src/main.py  ")
