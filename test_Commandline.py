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
    pattern = \
        """\t./test_Commandline.py command [-f ] [-i] [-k] [-b match] otherfile
    \t./test_Commandline.py make [-f] otherfile
    \t./test_Commandline.py install [-b match] otherfile"""

    cmd = Cmd(len(sys.argv), sys.argv, pattern)
    cmd.addCommandCall("make", make)
    cmd.addCommandCall("install", install)
    cmd.call()