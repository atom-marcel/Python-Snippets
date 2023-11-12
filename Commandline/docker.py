from typing import List, Dict, Any
import yaml
import json
from Commandline import cmd

class DockerCombine(object):
    files: List[str]
    yamlDict: Dict[str, Any]
    master: Dict[str, Any]

    def __init__(self):
        self.files = []
        self.yamlDict = {}
        self.master = {}

    def cmd(self, argc:int, argv: List[str]):
        c = cmd.Cmd(argc, argv, "docker-combine c -keys key1,key2,key3 -o outfile.yml files")
        keys = c.information["keys"].split(",")
        out = c.information["o"]
        self.addFiles(c.information["other"])
        self.combine(keys)
        self.saveMaster(out)


    def addFiles(self, files: List[str]):
        self.files = files
        
        for file in self.files:
            with open(file, "r") as f:
                obj = yaml.safe_load(f)
                self.yamlDict[file] = obj

    def combine(self, combinedKeys: List[str]):
        for key in combinedKeys:
            self.master[key] = []

        for file in self.yamlDict.keys():
            for key in self.yamlDict[file].keys():
                if key in combinedKeys and key in self.master:
                    self.master[key].append(self.yamlDict[file][key])
                else:
                    self.master[key] = self.yamlDict[file][key]

    def print(self):
        print(json.dumps(self.master, indent=4))

    def saveMaster(self, filename: str):
        with open(filename, "w") as f:
            yaml.safe_dump(self.master, f, sort_keys=False)

def startCombine(argc:int, argv:List[str]):
    dc = DockerCombine()
    dc.cmd(argc, argv)