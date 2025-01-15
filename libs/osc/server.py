from pythonosc import dispatcher,osc_server
from libs.effect import effect
import socket
class server():
 def __init__(self):
   self.ip = self.get_localip()
   self.port = 8000
   self.dispatcher = dispatcher.Dispatcher()
   self.effect = effect()
 def get_localip(self):
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    return ip
 def start(self):
    #self.dispatcher.map("/delay/time/1/fader*", self.effect.test_address_check)
    self.dispatcher.map("/*", self.effect.test_address_check)
   #  self.dispatcher.map("/delay/time/1/fader1", self.effect.test_address_check)
   #  self.dispatcher.map("/delay/*", self.effect.test_address_check)
    server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", self.port), self.dispatcher)#0.0.0.0 or self.ip
    print(f"OSC Server is running on {server.server_address}")
    print(f"OSC Server IP:{self.ip} PORT:{self.port}")
    server.serve_forever()                          