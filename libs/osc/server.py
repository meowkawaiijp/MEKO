import sounddevice as sd
import numpy as np
from pythonosc import dispatcher,osc_server
from threading import Thread
from effects import test_effect_delay
import socket
class server():
 def __init__(self):
   self.ip = self.get_localip()
   self.port = 8000
   self.dispatcher = dispatcher.Dispatcher()
 def get_localip(self):
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    return ip
 def start(self):
    self.dispatcher.map("/delay/time", test_effect_delay.test_effect_delay().set_delay_time)
    self.dispatcher.map("/delay/feedback", test_effect_delay.test_effect_delay().set_delay_feedback)
    server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", self.port), self.dispatcher)#0.0.0.0 or self.ip
    print(f"OSC Server is running on {server.server_address}")
    print(f"OSC Server IP:{self.ip} PORT:{self.port}")
    server.serve_forever()