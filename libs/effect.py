import json
import numpy as np
from libs.effects.Distortion import Distortion
from libs.effects.Equalizer import Equalizer
from libs.effects.Delay import Delay
from libs.effects.Compressor import Compressor
from libs.effects.Reverb import Reverb
from libs.effects.AutoWah import AutoWah
from libs.effects.Phaser import Phaser
from libs.effects.NoiseGate import NoiseGate

class EffectProcessor:
    def __init__(self):
        self.SETTINGS_FILE = "effect_settings.json"
        self.default_settings = {
            "base_volume": 2.0,
            "effects_chain": [
                {"name": "NoiseGate", "enabled": False, "params": {"threshold": 0.02}},
                {"name": "Phaser", "enabled": False, "params": {"rate": 0.5, "depth": 0.7}},
                {"name": "Distortion", "enabled": False, "params": {"drive": 10, "intensity": 1.0, "cutoff_freq": 8000, "fs": 44100, "apply_lowpass": True}},
                {"name": "Compressor", "enabled": False, "params": {"threshold": 0.5, "ratio": 4.0}},
                {"name": "Equalizer", "enabled": False, "params": {"lowcut": 100.0, "highcut": 1000.0, "fs": 44100}},
                {"name": "Delay", "enabled": False, "params": {"delay_time": 0.5, "feedback": 0.5}},
                {"name": "Reverb", "enabled": True, "params": {"reverb_amount": 0.5}},
                {"name": "AutoWah", "enabled": False, "params": {"mod_freq": 1.0}}
            ]
        }
        self.settings = self.load_settings()
        self.base_volume = self.settings["base_volume"]
        self.effects_instances = {
            "NoiseGate": NoiseGate,
            "Phaser": Phaser,
            "Distortion": Distortion,
            "Compressor": Compressor,
            "Equalizer": Equalizer,
            "Delay": Delay,
            "Reverb": Reverb,
            "AutoWah": AutoWah,
        }
        self.effects_chain = self.initialize_effects()

    def load_settings(self):
        try:
            with open(self.SETTINGS_FILE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("設定ファイルが見つからないため、デフォルト設定を使用します。")
            return self.default_settings

    def save_settings(self):
        with open(self.SETTINGS_FILE, "w") as file:
            json.dump(self.settings, file, indent=4)

    def initialize_effects(self):
        return [
            {"effect": self.effects_instances[entry["name"]](**entry["params"]), "enabled": entry["enabled"]}
            for entry in self.settings["effects_chain"]
        ]

    def audio_callback(self, indata, outdata, frames, time, status):
       # if status:
        #    print(f"ステータスエラー: {status}")
        self.settings = self.load_settings()
        self.effects_chain = self.initialize_effects()
        processed = np.zeros_like(indata)
        for channel in range(indata.shape[1]):
            signal = indata[:, channel]
            for effect_entry in self.effects_chain:
                if effect_entry["enabled"]:
                    signal = effect_entry["effect"].apply(signal)
            processed[:, channel] = signal

        outdata[:] = processed * self.base_volume

    def set_effect_state(self, effect_name, enabled):
        for entry in self.effects_chain:
            if entry["effect"].__class__.__name__ == effect_name:
                entry["enabled"] = enabled
                print(f"{effect_name} を {'有効化' if enabled else '無効化'}しました。")
                self.save_current_settings()
                return
        print(f"エフェクト {effect_name} が見つかりませんでした。")

    def update_effect_params(self, effect_name, params):
        for entry in self.effects_chain:
            if entry["effect"].__class__.__name__ == effect_name:
                for param, value in params.items():
                    setattr(entry["effect"], param, value)
                print(f"{effect_name} のパラメータを更新しました: {params}")
                self.save_current_settings()
                return
        print(f"エフェクト {effect_name} が見つかりませんでした。")

    def reorder_effects(self, new_order):
        if len(new_order) != len(self.effects_chain):
            print("エラー: 新しい順序の長さが一致しません。")
            return

        try:
            self.effects_chain = [self.effects_chain[i] for i in new_order]
            print(f"エフェクトの順序を変更しました: {new_order}")
            self.save_current_settings()
        except IndexError:
            print("エラー: 順序指定に無効なインデックスがあります。")

    def save_current_settings(self):
        self.settings["base_volume"] = self.base_volume
        self.settings["effects_chain"] = [
            {
                "name": entry["effect"].__class__.__name__,
                "enabled": entry["enabled"],
                "params": entry["effect"].__dict__,
            }
            for entry in self.effects_chain
        ]
        self.save_settings()

    def handle_osc_message(self, address, *args):
        osc_map = {
            "/1/toggle1": ("Distortion", bool(args[0])),
            #"/osc/osc": ("関数", パラメーター),
        }
        print(address)
        print(args)
        if address in osc_map:
            effect_name, enabled = osc_map[address]
            self.set_effect_state(effect_name, enabled)
        else:
            print(f"未知のOSCアドレス: {address}")
