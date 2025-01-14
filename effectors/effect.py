import numpy as np
from .Distortion import Distortion
from .Equalizer import Equalizer
from .Delay import Delay
from .Compressor import Compressor
from .Reverb import Reverb
from .AutoWah import AutoWah
from .Phaser import Phaser
from .FourierNoiseCanceller import FourierNoiseCanceller
def set_delay_time(address, *args):
    global delay_time  # 範囲: 0.1〜2.0
    delay_time=((args[0]) / 10)
    print(f"Delay time set to: {args[0]}")
   #  return delay_time
def set_delay_feedback(address, *args):
    global delay_feedback
    delay_feedback = ((args[0]) / 10) # 範囲: 0.0〜0.9
    print(f"Delay Feedback set to: {args[0]}")
   #  return delay_feedback
# パラメータを設定（必要に応じて変更）
base_volume = 1.0  # ボリューム
distortion = Distortion(drive=25, intensity=2)
compressor = Compressor(threshold=0.5, ratio=4.0)
equalizer = Equalizer(lowcut=100.0, highcut=1000.0, fs=44100)
delay = Delay(delay_time=0.5, feedback=0.5)
reverb = Reverb(reverb_amount=0.5)
auto_wah = AutoWah(mod_freq=1.0)
phaser = Phaser(rate=0.5, depth=0.7)
fourier_noise_canceller = FourierNoiseCanceller(noise_threshold=0.05, noise_reduction_factor=0.8)
def audio_callback(indata, outdata, frames, time, status):
    if status:
        print(status)
        
    global distortion, compressor, equalizer, delay, reverb, auto_wah
    processed = np.zeros_like(indata)

    # 各チャンネルにエフェクトを適用
    for channel in range(indata.shape[1]):
        signal = indata[:, channel]
        signal = phaser.apply(signal)
        signal = distortion.apply(signal)
        #signal = compressor.apply(signal)
        #signal = equalizer.apply(signal)
        #signal = delay.apply(signal)
        #signal = reverb.apply(signal)
        #signal = auto_wah.apply(signal)
        signal = fourier_noise_canceller.apply(signal)

        processed[:, channel] = signal

    outdata[:] = processed * base_volume
# def audio_callback(indata, outdata, frames, time, status):
#      global delay_buffer, reverb_buffer
#      if status:
#          print(status)
#      outdata[:] = indata * base_volume