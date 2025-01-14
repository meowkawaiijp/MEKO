import sounddevice as sd
import numpy as np
from pythonosc import dispatcher, osc_server
from threading import Thread
import socket
#あくまで動作検証用のコード後々高性能化

delay_time = 0.5      # ディレイタイム（秒）
delay_feedback = 0.3  # フィードバック量
reverb_amount = 0.2   # リバーブの量
buffer_size = 0       # バッファサイズ（後で自動設定）

delay_buffer = None
reverb_buffer = None

def select_device():
    print("\n=== 使用可能なデバイス一覧 ===")
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
         print(f"{i}: {dev['name']} ({'Input' if dev['max_input_channels'] > 0 else 'Output'})")
    print("=============================\n")

    input_device = int(input("使用する入力デバイス番号を入力してください: "))
    output_device = int(input("使用する出力デバイス番号を入力してください: "))
    return input_device, output_device

input_device, output_device = select_device()
input_samplerate = sd.query_devices(input_device)['default_samplerate']
output_samplerate = sd.query_devices(output_device)['default_samplerate']

if input_samplerate != output_samplerate:
     raise ValueError("入力デバイスと出力デバイスのサンプルレートが一致していません。")
sample_rate = int(input_samplerate)
buffer_size = int(sample_rate * 2)
delay_buffer = np.zeros(buffer_size)
reverb_buffer = np.zeros(buffer_size)

def set_delay_time(address, *args):
    global delay_time  # 範囲: 0.1〜2.0
    delay_time=((args[0] + 1) / 10)
    print(f"Delay time set to: {delay_time}")

def set_delay_feedback(address, *args):
    global delay_feedback
    delay_feedback = ((args[0]) / 10) # 範囲: 0.0〜0.9
    print(f"Delay Feedback set to: {delay_feedback}")

def set_reverb_amount(address, *args):
    global reverb_amount
    reverb_amount =((args[0]) / 10) # 範囲: 0.0〜1.0
    print(f"Reverb Amount set to: {reverb_amount}")

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/delay/time", set_delay_time)
dispatcher.map("/delay/feedback", set_delay_feedback)
dispatcher.map("/reverb/amount", set_reverb_amount)

def start_osc_server():
    server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", 8000), dispatcher)
    print(f"OSC Server is running on {server.server_address}")
    server.serve_forever()

def audio_callback(indata, outdata, frames, time, status):
     global delay_buffer, reverb_buffer

     if status:
         print(status)

     input_signal = indata[:, 0]  # モノラル入力を仮定

#     # ディレイ処理
     delay_samples = int(delay_time * sample_rate)
     delayed_signal = delay_buffer[:frames]
     delay_buffer[:-delay_samples] = delay_buffer[delay_samples:]
     delay_buffer[-delay_samples:] = input_signal + delay_feedback * delayed_signal

#     # リバーブ処理（ディレイを重ねる）
     reverb_signal = reverb_amount * delay_buffer[:frames]

     output_signal = input_signal + delayed_signal + reverb_signal
     outdata[:, 0] = output_signal

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
