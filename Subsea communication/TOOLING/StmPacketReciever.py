import struct
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

def parsepacket(data):
    # first byte is id
    # data folows until end
    #print("Packet: {}".format(data))
    id = data[0]
    data = data[1:]
    if id == 1:#message
        try:
            data = data.decode()
        except:
            pass
        print(data)
    elif id == 17:#imu_full
        try:
            data = struct.unpack("fffffff",data)
            print("IMU: {}".format(data))
        except:
            pass
    elif id == 21:#angles
        try:
            data = struct.unpack("ff",data)
            print("Angle: {}".format(data))
        except:
            pass
    else:
        print("Unknown packet {}: {}".format(id,data))
def main():
    #os.system("cls")
    while True:
        for port in GetStmPorts():
            try:
                serial = Serial(port, 115200, timeout=0.5)
            except:
                continue
            print("Opened port: {}".format(port))
            tick = 0
            databuffer = b""
            while True:
                try:
                    data = serial.read(1)
                    if data == b"\r":
                        if len(databuffer) == 0:
                            continue
                        parsepacket(databuffer)
                        databuffer = b""
                        continue
                    databuffer += data
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