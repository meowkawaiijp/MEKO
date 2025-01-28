import sounddevice as sd
from threading import Thread
from libs import setup
from libs.osc import server
import time
from libs import effect
import numpy as np
import sounddevice as sd
from threading import Thread
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
     callback=effect.EffectProcessor().audio_callback,
     device=(input_device, output_device) 
 )
 stream.start()
 osc_thread = Thread(target=server.server().start, daemon=True)
 osc_thread.start()
 try:
    print("オーディオを処理しています... 中止するには Ctrl+C を押してください。")
    while True:
        time.sleep(0.1)
        pass
 except KeyboardInterrupt:
    print("終了します...")
    stream.stop()
    stream.close()
if __name__ == "__main__":
    main()