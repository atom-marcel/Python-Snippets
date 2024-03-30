#!/env/python

import time
from Commandline.cmd import Cmd
import sys
import serial
from typing import Dict
from pynput.keyboard import Key, Listener
from threading import Thread

cmd: Cmd = None
loop: bool = False
thread: Thread = None
log: str = ""
ser: serial.Serial = None
mode: int = 0
view: str = ""
userInput: str = ""

def abort():
    global loop
    loop = False
    print("Exit...")

def onKeyPress(key: Key):
    if key == Key.esc:
        abort()

def onKeyRelease(key):
    if key == Key.esc:
        return False
    
def onDuplexKeyPress(key: Key):
    pass

def onDuplexKeyRelease(key: Key):
    global mode
    if(key == Key.enter):
        mode = 1

listener: Listener = Listener(onKeyPress, onKeyRelease)
listenerDuplex: Listener = None

def monitor(info: Dict):
    global loop
    baudrate = int(info["specifiers"]["b"])
    port = info["other"][0]

    listener.start()

    log = False
    if("log" in info["specifiers"]):
        log = True

    loop = True
    with serial.Serial(port, baudrate) as ser:
        while(loop):
            string = ""
            char = ser.read()
            while(char[-1] != 0):
                string += char.decode("ascii")
                char = ser.read()
            
            if(log):
                with open(info["specifiers"]["log"], "a", encoding="ascii") as f:
                    f.write(string)
            print(string, end="")

def sending(info: Dict):
    global loop
    baudrate = int(info["specifiers"]["b"])
    port = info["other"][0]
    loop = True

    listener.start()

    with serial.Serial(port, baudrate) as ser:
        while(loop):
            userInput = input("An das Board senden: ")
            ser.write(userInput.encode("ascii"))

def getRxAscii():
    c = ser.read()
    line = ""
    while(c[-1] != 0):
        line += c.decode("ascii")
        c = ser.read()
    return line

def updateView():
    global loop
    global view
    global mode
    global log

    while(loop):
        if(mode == 0):
            line = getRxAscii()
            log += f'RX\t{line}'
            view = log

        if(mode == 1):
            print('RX blocked')
            userInput = input("Usereingabe: ")
            ser.write(userInput.encode("ascii"))
            response = getRxAscii()
            log += f'TX\t{userInput}\n'
            log += f"RXR\t{response}"
            userInput = ""
            mode = 0

        print("\033c")
        print(view)

def dual(info: Dict):
    global loop
    global ser

    baudrate = int(info["specifiers"]["b"])
    port = info["other"][0]

    loop = True

    listenerDuplex = Listener(onDuplexKeyPress, onDuplexKeyRelease)
    listenerDuplex.start()
    listener.start()

    ser = serial.Serial(port, baudrate)

    updateView()

def main():
    global cmd
    pattern = \
    """\t./pyserialmonitor.py mode [-b baudrate] [-log logfile] port
    \t./pyserialmonitor.py monitor [-b baudrate] [-log logfile] port
    \t./pyserialmonitor.py sending [-b baudrate] port
    \t./pyserialmonitor.py dual [-b baudrate] port"""

    argc = len(sys.argv)
    argv = sys.argv
    cmd = Cmd(argc, argv, pattern)
    cmd.addCommandCall("monitor", monitor)
    cmd.addCommandCall("sending", sending)
    cmd.addCommandCall("dual", dual)
    cmd.call()

if __name__ == "__main__":
    main()