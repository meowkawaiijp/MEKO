import numpy as np

class Phaser:
    def __init__(self, rate=1.0, depth=1.0, fs=44100):
        """
        フェイザーエフェクトを初期化
        :param rate: フェーズシフトのモジュレーション速度（Hz）
        :param depth: モジュレーションの深さ
        :param fs: サンプリングレート（Hz）
        """
        self.rate = rate
        self.depth = depth
        self.fs = fs

    def set_parameters(self, rate, depth):
        """
        フェイザーエフェクトのパラメータを設定
        :param rate: フェーズシフトのモジュレーション速度（Hz）
        :param depth: モジュレーションの深さ
        """
        self.rate = rate
        self.depth = depth

    def apply(self, input: np.ndarray) -> np.ndarray:
        """
        フェイザーエフェクトを適用
        :param input: np.ndarray
            音声信号（np.float32: -1.0～1.0）
        :return: np.ndarray
            加工された音声信号
        """
        t = np.arange(len(input)) / self.fs
        phase_shift = np.sin(2 * np.pi * self.rate * t) * self.depth
        return input * (1 + phase_shift)