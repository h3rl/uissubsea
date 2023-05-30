import sys
import os
# Add the parent directory to the path so we can import the util package
sys.path.append(os.path.join(os.path.dirname(__file__),"../"))

import time

from util.serials import *
from serial import Serial

def processline(line):
    line = line.replace(",","\t").replace("\r","")
    return line+"\n"

def main():
    #os.system("cls")    
    while True:
        for port in GetStmPorts():
            try:
                serial = Serial(port, 115200, timeout=0.5)
            except:
                continue
            print("Opened port: {}".format(port))
            linebuffer = ""
            tick = 0
            while True:
                try:
                    data = serial.read(1)
                    data = data.decode()
                    if data == "\n":
                        continue
                    linebuffer += data
                    if data == "\r":
                        line = processline(linebuffer)
                        linebuffer = ""
                        print(line,end="")
                except:
                    pass

                tick += 1
                if tick > 1000:
                    if not port in GetStmPorts():
                        break
                    tick = 0
            print()
            print("Lost connection: {}".format(port))

if __name__ == "__main__":
    main()