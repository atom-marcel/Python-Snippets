from typing import Callable, Dict, List, Any
import pynput
import os

class Menu(object):

    callstackList: List[Callable] = []
    callstackDict: Dict[str, Callable] = {}
    name: str
    index: int = 0
    interact: bool = False

    calledIndex: int = 0
    lastInput: str = ""
    k_listener: pynput.keyboard.Listener

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
    
    def printMenu(self, mode: str = "default"):
        match mode:
            case "default":
                print(self.name)
                print("Es gibt folgende Menüpunkte:")
                for index, call in enumerate(self.callstackList):
                    string = [x for x in self.callstackDict.keys() if self.callstackDict[x] == call][0]
                    print(f"{index}\t{string}")
            case "interactive":
                print(self.name)
                print("Es gibt folgende Menüpunkte:")
                for index, call in enumerate(self.callstackList):
                    string = [x for x in self.callstackDict.keys() if self.callstackDict[x] == call][0]
                    if index == self.index:
                        print(f"->\t{index}\t{string}")
                    else:
                        print(f"\t{index}\t{string}")

    def clear(self):
        print("\033c", end="")

    def onKeyPress(self, key: pynput.keyboard.Key):
        match key:
            case pynput.keyboard.Key.up:
                if self.index > 0:
                    self.index -= 1
                    self.clear()
                    self.printMenu("interactive")
            case pynput.keyboard.Key.down:
                if self.index < len(self.callstackList) - 1:
                    self.index += 1
                    self.clear()
                    self.printMenu("interactive")
            case pynput.keyboard.Key.enter:
                self.k_listener.stop()
                self.callIndex(self.index)
                

    def onKeyRelease(self, key: pynput.keyboard.Key):
        match key:
            case pynput.keyboard.Key.esc:
                self.k_listener.stop()
    
    def menuInteract(self, mode: str = "default"):
        match mode:
            case "default":    
                self.clear()
                self.printMenu()
                self.keyboardInput()
            case "interactive":
                self.k_listener = pynput.keyboard.Listener(self.onKeyPress, self.onKeyRelease, True)
                self.clear()
                self.printMenu("interactive")
                self.k_listener.start()
                self.k_listener.join()

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