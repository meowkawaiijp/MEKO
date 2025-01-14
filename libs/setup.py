import sounddevice as sd
import numpy as np
from pythonosc import dispatcher, osc_server
from threading import Thread
import socket
class setup():
    def __init__(self):
        self.input_device, self.output_device = self.select_device()
        self.input_samplerate = None
        self.output_samplerate = None
        self.buffer_size = None
        self.sample_rate = None
    def select_device(self):
     #print("\n=== 使用可能なデバイス一覧 ===")
     devices = sd.query_devices()
     for i, dev in enumerate(devices):
         print(f"{i}: {dev['name']} ({'Input' if dev['max_input_channels'] > 0 else 'Output'})")
     #print("=============================\n")

     #input_device = int(input("使用する入力デバイス番号を入力してください: "))
     #output_device = int(input("使用する出力デバイス番号を入力してください: "))
     input_device = 1
     output_device = 1
     return input_device, output_device
    def device_setup(self):
        self.input_samplerate = sd.query_devices(self.input_device)['default_samplerate']
        self.output_samplerate = sd.query_devices(self.output_device)['default_samplerate']
        print(f"input samplerate: {self.input_samplerate} output samplerate: {self.output_samplerate}")
        if self.input_samplerate != selfoutput_samplerate:
            ValueError("input samplerateとoutputsamplerateの値が一致しません。")
        self.sample_rate = int(self.input_samplerate)
        self.buffer_size = int(self.sample_rate * 2)
        #self.delay_buffer = np.zeros(buffer_size)
        #self.reverb_buffer = np.zeros(buffer_size)
    def effect_preset(self):
        dispatcher = dispatcher.Dispatcher()
        #for effectname,effectargs in zip(""):
        dispatcher.map("/delay/time", set_delay_time)
        dispatcher.map("/delay/feedback", set_delay_feedback)
        dispatcher.map("/reverb/amount", set_reverb_amount)
