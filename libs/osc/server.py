from pythonosc import dispatcher,osc_server
from effectors import effect
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
    self.dispatcher.map("/delay/time", effect.set_delay_time)
    self.dispatcher.map("/delay/feedback", effect.set_delay_feedback)
    server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", self.port), self.dispatcher)#0.0.0.0 or self.ip
    print(f"OSC Server is running on {server.server_address}")
    print(f"OSC Server IP:{self.ip} PORT:{self.port}")
    server.serve_forever()