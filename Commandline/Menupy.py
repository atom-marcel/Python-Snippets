from typing import Callable, Dict, List, Any

class Menu(object):

    callstackList: List[Callable] = []
    callstackDict: Dict[str, Callable] = {}
    name: str

    calledIndex: int = 0
    lastInput: str = ""

    def __init__(self, name:str):
        self.name = name

    def addCallable(self, key: str, call: Callable) -> int:
        self.callstackList.append(call)
        self.callstackDict[key] = call

        return [i for i,x in enumerate(self.callstackList) if x == call][0]

    def callIndex(self, index: int) -> Any:
        return self.callstackList[index]()
    
    def callKey(self, key: str) -> Any:
        return self.callstackDict[key]()
    
    def printMenu(self):
        print(self.name)
        print("Es gibt folgende Menüpunkte:")
        for index, call in enumerate(self.callstackList):
            string = [x for x in self.callstackDict.keys() if self.callstackDict[x] == call][0]
            print(f"{index}\t{string}")

    def clear(self):
        print("\033c")
    
    def menuInteract(self):
        self.clear()
        self.printMenu()
        self.keyboardInput()

    def invalidInput(self):
        self.clear()
        print("Die Eingabe war ungültig, bitte gültige Zahl eingeben.")
        self.printMenu()
        self.keyboardInput()

    def keyboardInput(self):
        self.lastInput = input("Menüpunkt wählen: ")
        
        try:
            self.calledIndex = int(self.lastInput)
            if(self.calledIndex != None):
                if(self.calledIndex < len(self.callstackList)):
                    self.callIndex(self.calledIndex)
                    # call and clean exit
                    return
            
            # integer check failed
            self.invalidInput()
        except:
            # try failed
            self.invalidInput()



