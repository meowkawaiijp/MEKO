import json
import numpy as np
from ..effects.Distortion import Distortion
from ..effects.Equalizer import Equalizer
from ..effects.Delay import Delay
from ..effects.Compressor import Compressor
from ..effects.Reverb import Reverb
from ..effects.AutoWah import AutoWah
from ..effects.Phaser import Phaser
from ..effects.NoiseGate import NoiseGate

# 動的にエフェクトをいじれるようにするためのコード。OSCの信号からエフェクトの状態を変更する。

class effect():
    def __init__(self):
        self.SETTINGS_FILE = "effect_settings.json"
        self.default_settings = {
            "base_volume": 1.0,
            "effects_chain": [
                {"name": "NoiseGate", "enabled": False, "params": {"threshold": 0.02}},
                {"name": "Phaser", "enabled": False, "params": {"rate": 0.5, "depth": 0.7}},
                {"name": "Distortion", "enabled": True, "params": {"drive": 10, "intensity": 1.0, "cutoff_freq": 8000, "fs": 44100, "apply_lowpass": True}},
                {"name": "Compressor", "enabled": False, "params": {"threshold": 0.5, "ratio": 4.0}},
                {"name": "Equalizer", "enabled": False, "params": {"lowcut": 100.0, "highcut": 1000.0, "fs": 44100}},
                {"name": "Delay", "enabled": False, "params": {"delay_time": 0.5, "feedback": 0.5}},
                {"name": "Reverb", "enabled": False, "params": {"reverb_amount": 0.5}},
                {"name": "AutoWah", "enabled": False, "params": {"mod_freq": 1.0}}
            ]
        }
        self.settings = self.load_settings()
        self.base_volume = self.settings["base_volume"]
        self.effects_instances = {
            "NoiseGate": NoiseGate(**self.settings["effects_chain"][0]["params"]),
            "Phaser": Phaser(**self.settings["effects_chain"][1]["params"]),
            "Distortion": Distortion(**self.settings["effects_chain"][2]["params"]),
            "Compressor": Compressor(**self.settings["effects_chain"][3]["params"]),
            "Equalizer": Equalizer(**self.settings["effects_chain"][4]["params"]),
            "Delay": Delay(**self.settings["effects_chain"][5]["params"]),
            "Reverb": Reverb(**self.settings["effects_chain"][6]["params"]),
            "AutoWah": AutoWah(**self.settings["effects_chain"][7]["params"]),
        }
        self.effects_chain = [
            {"effect": self.effects_instances[entry["name"]], "enabled": entry["enabled"]}
            for entry in self.settings["effects_chain"]
        ]

    def load_settings(self):
        try:
            with open(self.SETTINGS_FILE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("設定ファイルが存在しないか、読み込めませんでした。デフォルト設定を使用します。")
            return self.default_settings

    def save_settings(self, settings):
        with open(self.SETTINGS_FILE, "w") as file:
            json.dump(settings, file, indent=4)

    def audio_callback(self, indata, outdata, frames, time, status):
        if status:
            print(f"ステータスエラー: {status}")
        global effects_chain
        processed = np.zeros_like(indata)
        for channel in range(indata.shape[1]):
            signal = indata[:, channel]
            for effect_entry in effects_chain:
                if effect_entry["enabled"]:
                    signal = effect_entry["effect"].apply(signal)
            processed[:, channel] = signal
        outdata[:] = processed * self.base_volume

    def set_effect_state(self, effect_name, enabled):
        global effects_chain
        for entry in effects_chain:
            if entry["effect"].__class__.__name__ == effect_name:
                entry["enabled"] = enabled
                print(f"{effect_name} の有効状態を設定: {enabled}")
                break
        self.save_current_settings()

    def update_effect_params(self, effect_name, params):
        global effects_chain
        for entry in effects_chain:
            if entry["effect"].__class__.__name__ == effect_name:
                for param, value in params.items():
                    setattr(entry["effect"], param, value)
                print(f"{effect_name} のパラメータを更新: {params}")
                break
        self.save_current_settings()

    def reorder_effects(self, new_order):
        global effects_chain
        if len(new_order) != len(effects_chain):
            print("エラー: 新しい順序の長さがエフェクトチェーンの長さと一致しません。")
            return

        try:
            effects_chain = [effects_chain[i] for i in new_order]
            print(f"エフェクトの順序を変更しました: {new_order}")
            self.save_current_settings()
        except IndexError:
            print("エラー: 新しい順序に無効な値があります。")

    def save_current_settings(self):
        global effects_chain
        self.settings["base_volume"] = self.base_volume
        self.settings["effects_chain"] = [
            {
                "name": entry["effect"].__class__.__name__,
                "enabled": entry["enabled"],
                "params": entry["effect"].__dict__,
            }
            for entry in effects_chain
        ]
        self.save_settings(self.settings)
    def test_address_check(self,address, *args):
        print("受信したOSC値:")
        print(address)
        print(args)
# 使用例
#==========================
# # エフェクト順序を変更 (例: [Distortion → Delay → Compressor → Reverb])
# reorder_effects([2, 5, 3, 6])

# # 新しい順序でエフェクトを適用する
# set_effect_state("Reverb", True)
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