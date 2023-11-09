from Commandline.cmd import Cmd
import json
from typing import Dict
import sys

def make(info: Dict):
    print("Make called, additional Items:")
    print(info["other"])

    print(json.dumps(info, indent=4))

def install(info: Dict):
    print("Install called, additional Items:")

    print(info["other"])

if __name__ == "__main__":
    cmd = Cmd(len(sys.argv), sys.argv, "./test_Commandline.py command [-f additional_file] [-i] [-k] [-b match] otherfiles\n./test_Commandline.py make\n./test_Commandline.py install")
    cmd.addCommandCall("make", make)
    cmd.addCommandCall("install", install)
    cmd.call()