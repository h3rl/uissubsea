import os
import sys
import threading

#Example:
"""
vr = GstreamerTopside(GSTREAMER_CONFIG, supress_output=True)
vr.start()
vr.stop()

vt = GstreamerJetson(GSTREAMER_CONFIG)
vt.start()
vt.start()
"""

#TODO make work for topside depending on os

UDPcommandTopside = 'gst-launch-1.0 -v udpsrc port={0} ! "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! h264parse ! decodebin ! videoconvert ! autovideosink sync=false'
UDPcommandJetson = "gst-launch-1.0 nvarguscamerasrc sensor-id=0 ! 'video/x-raw(memory:NVMM), width={0}, heigth={1}, framerate={2}, format=NV12' ! nvv4l2h264enc insert-sps-pps=true bitrate={3} ! rtph264pay ! udpsink host={4} port={5}"

class GstreamerConfig:
    def __init__(self, ip:str = "192.168.0.145"):
        self.destination_ip = ip
        self.destination_port = 5000
        self.width = 1920
        self.height = 1080
        self.framerate = 30
        self.bitrate = 40e6 #def 4-10mpbs, sports 20-40mpbs

        self.verify()

    def verify(self):
        if self.destination_ip is None:
            raise Exception("GstreamerConfig: destination_ip is not set")
        elif str(self.destination_ip).count(".") < 3:
            raise Exception("GstreamerConfig: destination_ip is not valid")
        if self.destination_port is None:
            raise Exception("GstreamerConfig: destination_port is not set")

GSTREAMER_CONFIG = GstreamerConfig()

class GstreamerJetson:
    def __init__(self, config: GstreamerConfig = GSTREAMER_CONFIG):
        self.destination_ip = config.destination_ip
        self.destination_port = config.destination_port
        self.width = config.width
        self.height = config.height
        self.framerate = config.framerate
        self.bitrate = config.bitrate

    def start(self):
        print("Starting gstreamer videostream")
        os.system(UDPcommandJetson.format(self.width, self.height, self.framerate, self.bitrate, self.destination_ip, self.destination_port))
    
class GstreamerTopside:
    def __init__(self, config:GstreamerConfig = GSTREAMER_CONFIG, supress_output:bool = True):
        self.destination_port = config.destination_port
        self.supress_output = supress_output

    def start(self):
        # Start the gstreamer pipeline
        print("Starting gstreamer reciever...")
        if self.supress_output:
            open(os.devnull, 'w')
            os.system(UDPcommandTopside.format(self.destination_port) + " > /dev/null 2>&1")
        else:
            os.system(UDPcommandTopside.format(self.destination_port))

    def start_noblock(self):
        start_thread = threading.Thread(target=self.start)
        start_thread.start()

    def stop(self):
        print("Stopping gstreamer videostream")
        if self.supress_output:
            open(os.devnull, 'w')
            os.system("taskkill /F /IM \"gst-launch-1.0.exe\" /t /fi \"status eq running\" > nul")
        else:
            os.system("taskkill /F /IM \"gst-launch-1.0.exe\"")