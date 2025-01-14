import sounddevice as sd
import numpy as np
from pythonosc import dispatcher, osc_server
from threading import Thread
import socket
from libs import server,effect_setup,setup
def audio_callback(indata, outdata, frames, time, status):
     global delay_buffer, reverb_buffer
     if status:
         print(status)
#      input_signal = indata[:, 0]  # モノラル入力を仮定
# #     # ディレイ処理
#      delay_samples = int(delay_time * sample_rate)
#      delayed_signal = delay_buffer[:frames]
#      delay_buffer[:-delay_samples] = delay_buffer[delay_samples:]
#      delay_buffer[-delay_samples:] = input_signal + delay_feedback * delayed_signal

# #     # リバーブ処理（ディレイを重ねる）
#      reverb_signal = reverb_amount * delay_buffer[:frames]

#      output_signal = input_signal + delayed_signal + reverb_signal
#      outdata[:, 0] = output_signal
def main():
 input_device,output_device = 
 stream = sd.Stream(
     samplerate=sample_rate,
     channels=1,  # モノラル
     dtype='float32',
     latency='low',
     callback=audio_callback,
     device=(input_device, output_device) 
 )
 stream.start()
 osc_thread = Thread(target=start_osc_server, daemon=True)
 osc_thread.start()
 try:
    print("Processing audio... Press Ctrl+C to stop.")
    while True:
        pass
 except KeyboardInterrupt:
    print("Exiting...")
    stream.stop()
    stream.close()
