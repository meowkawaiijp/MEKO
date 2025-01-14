import sounddevice as sd
import numpy as np
from pythonosc import dispatcher, osc_server
from threading import Thread
import socket
class server():
 def __init__(self):
   self.ip = self.get_localip()
 def get_localip(self):
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    return ip
 def start(self):
    server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", self.port), dispatcher)#0.0.0.0 or self.ip
    print(f"OSC Server is running on {server.server_address}")
    print(f"OSC Server IP:{self.ip} PORT:{self.port}")
    server.serve_forever()