from typing import Dict, List, Callable, Any
import re
import json

class Cmd(object):
    argc: int
    argv: List[str] = []

    specifiers: Dict[str, str] = {}
    command: str = ""
    other: List[str] = []
    pattern: str = ""

    information: Dict = {}

    def __init__(self, argc: int, argv: List[str], pattern: str):
        self.argc = argc
        self.argv = argv
        self.pattern = pattern
        if self.checkValidation():
            self.parseArgs()

    def checkValidation(self):
        if self.argc <= 2:
            print("Zu wenige Argumente wurden übergeben!")
            print(self.pattern)
            return False
        
        return True

    def addSpecifier(self, specifier: str, value: str):
        self.specifiers[specifier] = value
        self.information["specifiers"] = self.specifiers

    def addCommand(self, command: str):
        self.command = command
        self.information["command"] = command

    def addOther(self, other: str):
        self.other.append(other)
        self.information["other"] = self.other

    def parseArgs(self):
        self.addCommand(self.argv[1])
        lastSpec = None
        for i, arg in enumerate(self.argv):
            if arg[0] == "-":
                self.addSpecifier(arg[1:], self.argv[i + 1])
                lastSpec = arg[1:]
                continue

            if lastSpec != None:
                if arg == self.specifiers[lastSpec]:
                    continue

            if i > 0 and arg != self.command:
                self.addOther(arg)

    def print(self):
        print(json.dumps(self.information, indent=4))
            