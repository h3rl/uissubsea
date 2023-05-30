from serial.tools import list_ports

def GetStmPorts():
    ports = list_ports.comports()
    wanted = []
    for port, desc, hwid in sorted(ports):
        if "STMicroelectronics" in desc:
            wanted.append(port)
            #print("{}: {} [{}]".format(port, desc, hwid))
    return wanted