import sys
import os
# Add the parent directory to the path so we can import the util package
sys.path.append(os.path.join(os.path.dirname(__file__),"../"))

from threading import Thread
import time
import struct
from serial import Serial
from collections import deque

from util.gstreamer import *
from util.packets import *
from util.serials import *

# plan
"""
Threads:
    - SerialsHandler (check for new serials)
    - Serials (read and write)
    - Gstreamer (send video)
    - UDP (send info packets to topside)

"""
#TODO: figure out where to packets to serials who want it

# Global variables
SERIAL_RECEIVED_PACKETS = deque(maxlen=1024)
OPEN_SERIALS = []

def thread_serials_handler():
    global OPEN_SERIALS
    while True:
        # remove closed ports
        new_open_serials = []
        for serial in OPEN_SERIALS:
            if not serial.closed:
                new_open_serials.append(serial)
                continue
            print("Closed port: {}".format(serial.port))

        if len(new_open_serials) != len(OPEN_SERIALS):
            OPEN_SERIALS = new_open_serials

        ports = GetStmPorts()
        for port in ports:
            if port in [serial.port for serial in OPEN_SERIALS]:
                continue

            # add to OPEN_SERIALS
            serial = Serial(port, 115200, timeout=0.5)
            OPEN_SERIALS.append(serial)
            print("Opened port: {}".format(port))
        time.sleep(5)

def thread_serials():
    global OPEN_SERIALS
    while True:
        for serial in OPEN_SERIALS:
            if serial.closed:
                continue

            if not serial.readable():
                continue
            
            _id = serial.read(1)
            id = struct.unpack("B", _id)[0]
            if id not in PACKETIDS:
                raise Exception("Invalid packet id")
            size = PACKETIDS[id].size
            bytes_data = serial.read(size, timeout=0.1)
            if len(bytes_data) != size:
                raise Exception("Packet size not as expected")
            
            packet = Packet()
            packet.id = id
            packet.data = bytes_data

            print("Received packet: {}".format(packet))
            SERIAL_RECEIVED_PACKETS.append(packet)

#TODO: implement
def thread_udp():
    pass

def thread_gstreamer():
    gstr_cfg = GstreamerConfig("192.168.0.145")
    gstr = GstreamerJetson(gstr_cfg)
    gstr.start()

def main():
    # Start all threads
    serials_handler_thread = Thread(target=thread_serials_handler)
    serials_handler_thread.start()

    serial_thread = Thread(target=thread_serials)
    serial_thread.start()

    gstreamer_thread = Thread(target=thread_gstreamer)
    gstreamer_thread.start()

    udp_thread = Thread(target=thread_udp)
    udp_thread.start()

if __name__ == "__main__":
    main()