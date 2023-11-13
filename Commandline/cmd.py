from typing import Dict, List, Callable, Any
import re
import json

class Cmd(object):
    argc: int
    argv: List[str] = []

    specifiers: Dict[str, List|Dict] = {}
    # not needed 
    #specifiers["arg"] = {}
    #specifiers["static"] = []

    command: str = ""
    other: List[str] = []
    pattern: str = ""
    validationPrint: bool = False

    information: Dict = {}

    cmdCommands: Dict[str, Callable] = {}

    def __init__(self, argc: int, argv: List[str], pattern: str):
        self.argc = argc
        self.argv = argv
        self.pattern = pattern
        if self.checkValidation():
            # not needed
            #self.analyzePattern()
            self.parseArgs()

    def checkValidation(self):
        if self.argc <= 2 and not self.validationPrint:
            self.validationPrint = True
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

    def analyzePattern(self):
        specifiers: List[str] = re.findall(r"\[\S+\]|\[\S+ \S+\]", self.pattern)
        for spec in specifiers:
            spec = spec.replace("[", "")
            spec = spec.replace("]", "")
            element = spec.split(" ")
            if(len(element) >= 2):
                self.specifiers["arg"][element[0][1:]] = element[1]
            else:
                self.specifiers["static"].append(element[0][1:])

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

    def checkSpecifier(self, spec: str):
        if spec in self.information["specifiers"]:
            return True
        
        return False

    def getSpecifierArg(self, spec: str):
        return self.information["specifiers"][spec]

    def getAdditionalArgs(self):
        return self.information["other"]
    
    def addCommandCall(self, command: str, call: Callable):
        self.cmdCommands[command] = call

    def call(self):
        if self.command in self.cmdCommands:
            self.cmdCommands[self.command](self.information)
        else:
            print("Es gibt keinen Funktionsaufruf für dieses Kommando")
            print(self.pattern)

    def print(self):
        print(json.dumps(self.information, indent=4))
            