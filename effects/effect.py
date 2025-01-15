import numpy as np
from .Distortion import Distortion
from .Equalizer import Equalizer
from .Delay import Delay
from .Compressor import Compressor
from .Reverb import Reverb
from .AutoWah import AutoWah
from .Phaser import Phaser
from .NoiseGate import NoiseGate
#動的にエフェクトをいじれるようにするためのコード。oscの信号からエフェクトの状態を変更する。

#TODO oscの信号を受け取ってエフェクトの値をいじれるようにする。
base_volume = 1.0
distortion = Distortion(drive=10, intensity=1.0, cutoff_freq=8000, fs=44100, apply_lowpass=True)
compressor = Compressor(threshold=0.5, ratio=4.0)
equalizer = Equalizer(lowcut=100.0, highcut=1000.0, fs=44100)
delay = Delay(delay_time=0.5, feedback=0.5)
reverb = Reverb(reverb_amount=0.5)
auto_wah = AutoWah(mod_freq=1.0)
phaser = Phaser(rate=0.5, depth=0.7)
noise_gate = NoiseGate(threshold=0.02)
effects_chain = [
    {"effect": noise_gate, "enabled": False},
    {"effect": phaser, "enabled": False},
    {"effect": distortion, "enabled": True},
    {"effect": compressor, "enabled": False},
    {"effect": equalizer, "enabled": False},
    {"effect": delay, "enabled": False},
    {"effect": reverb, "enabled": False},
    {"effect": auto_wah, "enabled": False},
]
def audio_callback(indata, outdata, frames, time, status):
    if status:
        print(status)
        
    global effects_chain
    processed = np.zeros_like(indata)
    for channel in range(indata.shape[1]):
        signal = indata[:, channel]
        for effect_entry in effects_chain:
            if effect_entry["enabled"]:
                signal = effect_entry["effect"].apply(signal)

        processed[:, channel] = signal

    outdata[:] = processed * base_volume
def set_effect_state(effect_name, enabled):
    for effect_entry in effects_chain:
        if effect_entry["effect"].__class__.__name__ == effect_name:
            effect_entry["enabled"] = enabled
            print(f"{effect_name} enabled: {enabled}")
def reorder_effects(new_order):
    global effects_chain
    effects_chain = [effects_chain[i] for i in new_order]
    print("Effects reordered.")

#使用例

#==========================
# # ノイズゲートを無効化
# set_effect_state("NoiseGate", False)

# # リバーブを有効化
# set_effect_state("Reverb", True)

# # エフェクトの順序を [Distortion → Delay → Compressor → Reverb] に変更
# reorder_effects([2, 5, 3, 6])

#==========================



#def set_delay_time(address, *args):
#     global delay_time  # 範囲: 0.1〜2.0
#     delay_time=((args[0]) / 10)
#     print(f"Delay time set to: {args[0]}")
#    #  return delay_time
# def set_delay_feedback(address, *args):
#     global delay_feedback
#     delay_feedback = ((args[0]) / 10) # 範囲: 0.0〜0.9
#     print(f"Delay Feedback set to: {args[0]}")