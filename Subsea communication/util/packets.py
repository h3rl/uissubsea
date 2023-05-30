import struct

#Example:
"""
magx = 1212
magy = 1313
magpacket = CreatePacket("Magnometer", magx, magy)
#eller
#magpacket = CreatePacket(12, magx, magy)
print(magpacket) # b'\x0c\xbc\x04!\x05'

# and parse it
packet = ParsePacket(magpacket)
print(packet) # 12: (1212, 1313)
"""

class PacketId:
    def __init__(self, id, name, struct_format) -> None:
        self.id = id
        self.name = name
        self.struct_format = struct_format
        self.size = struct.calcsize(struct_format)

PACKETIDS = {}
PACKETNAME2ID = {}

def PacketIdsAppend(id, name, struct_format):
    global PACKETIDS
    global PACKETNAME2ID
    PACKETIDS[id] = PacketId(id, name, struct_format)
    PACKETNAME2ID[name] = id

#TODO: add more packets
# format: https://docs.python.org/3/library/struct.html
# Topside to Jetson
PacketIdsAppend(1, "Ping", "s")
PacketIdsAppend(2, "Pong", "s")
PacketIdsAppend(3, "Joystick", "ddd")
# PacketIdsAppend(4,"InitCamerastream","")

# Jetson to Topside
PacketIdsAppend(10, "Accelerometer", "hhh")
PacketIdsAppend(11, "Gyro", "hhh")
PacketIdsAppend(12, "Magnometer", "hh")
PacketIdsAppend(13, "Barometer", "h")
PacketIdsAppend(14, "Temperature", "h")
PacketIdsAppend(15, "Humidity", "h")

PacketIdsAppend(20, "Thrust", "hhhhhh")
PacketIdsAppend(21, "Angle", "dd")
PacketIdsAppend(22, "TargetAngle", "dd")

PacketIdsAppend(30, "Voltage", "f")
PacketIdsAppend(31, "Current", "f")
PacketIdsAppend(32, "Power", "f")

class Packet:
    def __init__(self) -> None:
        self.id = 0
        self.data = None
    
    def serialize(self, args):
        # check valid id
        if self.id not in PACKETIDS:
            raise Exception("Invalid packet id")
        # check valid data

        struct_format = PACKETIDS[self.id].struct_format
        if len(args) != len(struct_format):
            raise Exception("Invalid packet data")
        
        # B gives 255 values for id and size in bytes
        self.data = struct.pack("B", self.id)
        self.data += struct.pack(struct_format, *args)
        return self.data
    
    def deserialize(self, data):
        id = struct.unpack("B", data[0:1])[0]
        if id not in PACKETIDS:
            raise Exception("Invalid packet id")
        struct_format = PACKETIDS[id].struct_format
        args = struct.unpack(struct_format, data[1:])

        # create packet
        self.id = id
        self.data = args
        return self

    def __str__(self) -> str:
        return f"{self.id}: {self.data}"

def CreatePacket(id, *data):
    # convert id to int if string
    if type(id) == str and id in PACKETNAME2ID:
        id = PACKETNAME2ID[id]
    if id not in PACKETIDS:
        raise Exception("Invalid packet id")
    packet = Packet()
    packet.id = id
    return packet.serialize(data)

def ParsePacket(id,data):
    if id not in PACKETIDS:
        raise Exception("Invalid packet id")
    packet = Packet()
    return packet.deserialize(data)


def CreateCHeaderPacketIds():
    
    with open("packetbuilder.h", "r+") as f:
        lines = f.readlines()
        p1 = 0
        p2 = 0
        for line in lines:
            if "Start PacketIds" in line:
                p1 = lines.index(line)
            elif "End PacketIds" in line:
                p2 = lines.index(line)
    

    with open("packetbuilder.h", "r+") as f:
        lines = f.readlines()
        p1 = 0
        p2 = 0
        for line in lines:
            if "Start PacketInfo" in line:
                p1 = lines.index(line)
            elif "End PacketInfo" in line:
                p2 = lines.index(line)
        
        # remove inbetween
        header_start = lines[:p1+1]
        header_end = lines[p2:]

        to_add = []

        to_add.append("enum PacketIds {\n")
        # parse PACKETIDS and add to lines
        for id in PACKETIDS:
            packet = PACKETIDS[id]
            to_add.append(f"    {packet.name.upper()} = {packet.id},\n")
        to_add.append("};\n")

        to_add.append("\n")

        to_add.append("enum PacketSize {\n")
        for id in PACKETIDS:
            packet = PACKETIDS[id]
            to_add.append(f"    {packet.name.upper()} = {packet.size},\n")
        to_add.append("};\n")

        # write to file
        to_write = header_start + to_add + header_end
        f.seek(0)
        f.truncate()
        f.writelines(to_write)
        f.close()

CreateCHeaderPacketIds()