from typing import Dict, List, Any
import json

class Cfg(object):
    path: str
    information: Dict[str, Dict] = {}
    rawString: str = ""

    def __init__(self, path: str) -> None:
        self.path = path

    def loadFile(self):
        with open(self.path, "r") as f:
            self.rawString = f.read()

    def rawStringToInformation(self): 
        isKey: bool = False
        isTopic: bool = False
        lastTopic: str = ""
        lastToken: str = ""
        lastKey: str = ""

        lines: List[str] = self.rawString.splitlines()
        print(lines)

        for line in lines:
            line = line.strip()
            for i, c in enumerate(line):
                if c == "[":
                    isTopic = True
                    continue
                
                if c == "]" and isTopic:
                    lastTopic = lastToken
                    self.information[lastToken] = {}
                    isTopic = False
                    lastToken = ""
                    break

                if c == "=":
                    isKey = True
                
                if isKey:
                    lastKey = lastToken
                    self.information[lastTopic][lastKey] = ""
                    isKey = False
                    lastToken = ""
                    continue

                if i == len(line) - 1:
                    lastToken += c
                    self.information[lastTopic][lastKey] = lastToken
                    lastToken = ""
                    break

                lastToken += c

    def informationToRawString(self):
        self.rawString = ""
        for topic in self.information:
            self.rawString += "[" + topic + "]" + "\n"

            for key in self.information[topic]:
                self.rawString += key + "=" + self.information[topic][key] + "\n"
            
            self.rawString += "\n"

    def saveFile(self):
        with open(self.path, "w") as f:
            f.write(self.rawString)

    def print(self):
        print(json.dumps(self.information, indent=4))