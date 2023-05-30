from packets import *

#TODO add more parsers
#TODO add examples

def ParseGyroPacket(packet: Packet):
    if packet.id != PACKETNAME2ID["GYRO"]:
        raise Exception("Invalid packet id")
    return packet.data