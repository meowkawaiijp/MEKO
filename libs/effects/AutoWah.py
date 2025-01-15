import numpy as np
class AutoWah:
    def __init__(self, mod_freq=1.0, fs=44100):
        self.mod_freq = mod_freq
        self.fs = fs

    def set_parameters(self, mod_freq):
        """
        オートワウのパラメータを設定する
        :param mod_freq: float
            モジュレーション周波数（Hz）
        """
        self.mod_freq = mod_freq

    def apply(self, input: np.ndarray) -> np.ndarray:
        """
        オートワウエフェクトを適用する
        :param input: np.ndarray
            音声信号
        :return: np.ndarray
            加工された音声信号
        """
        t = np.arange(len(input)) / self.fs
        mod_signal = np.sin(2 * np.pi * self.mod_freq * t) * 0.5 + 0.5
        output = input * mod_signal
        return output
