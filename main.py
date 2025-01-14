import sounddevice as sd
import numpy as np
from pythonosc import dispatcher, osc_server
from threading import Thread
import socket
from libs import setup
from libs.osc import server
import time
from effectors import effect
import numpy as np
import sounddevice as sd
from wave import Wave_read, open
from threading import Thread
from enum import Enum
#----------------------------
#ラズパイの方でspiの有効化をする。
#ipadosのtouchoscを購入する。
#----------------------------

def main():
 s = setup.setup()
 input_device,output_device = s.select_device()
 input_samplerate,output_samplerate,sample_rate,buffer_size =s.device_setup()
 stream = sd.Stream(
     samplerate=sample_rate,
     channels=1,  # モノラル
     dtype='float32',
     latency='low',
     callback=effect.audio_callback,
     device=(input_device, output_device) 
 )
 stream.start()
 osc_thread = Thread(target=server.server().start, daemon=True)
 osc_thread.start()
 try:
    print("Processing audio... Press Ctrl+C to stop.")
    while True:
        time.sleep(0.1)
        pass
 except KeyboardInterrupt:
    print("Exiting...")
    stream.stop()
    stream.close()
if __name__ == "__main__":
    main()