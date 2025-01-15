import sounddevice as sd
class setup():
    def __init__(self):
        self.input_device, self.output_device = self.select_device()
        self.input_samplerate,self.output_samplerate,self.sample_rate,self.buffer_size =self.device_setup()
    def select_device(self):
     #print("使用可能なデバイス一覧")
     devices = sd.query_devices()
     for i, dev in enumerate(devices):
         print(f"{i}: {dev['name']} ({'Input' if dev['max_input_channels'] > 0 else 'Output'})")
     #input_device = int(input("使用する入力デバイス番号を入力してください: "))
     #output_device = int(input("使用する出力デバイス番号を入力してください: "))
     input_device = 1
     output_device = 1
     return input_device, output_device
    def device_setup(self):
        self.input_samplerate = sd.query_devices(self.input_device)['default_samplerate']
        self.output_samplerate = sd.query_devices(self.output_device)['default_samplerate']
        print(f"input samplerate: {self.input_samplerate} output samplerate: {self.output_samplerate}")
        if self.input_samplerate != self.output_samplerate:
            ValueError(f"input samplerateとoutput samplerateの値が一致しません。 {self.input_samplerate} !={self.output_samplerate}")
        self.sample_rate = int(self.input_samplerate)
        self.buffer_size = int(self.sample_rate * 2)
        #self.delay_buffer = np.zeros(buffer_size)
        #self.reverb_buffer = np.zeros(buffer_size)
        return self.input_samplerate,self.output_samplerate,self.sample_rate,self.buffer_size