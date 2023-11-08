from Commandline.cmd import Cmd
import sys

if __name__ == "__main__":
    cmd = Cmd(len(sys.argv), sys.argv, "./test_Commandline.py command [-f additional_file] otherfiles")
    cmd.print()