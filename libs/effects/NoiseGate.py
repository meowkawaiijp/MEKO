import numpy as np
class NoiseGate:
    def __init__(self, threshold=0.05):
        """
        ノイズゲートを初期化します。
        :param threshold: float
            信号をカットするしきい値（0.0～1.0）
        """
        self.threshold = threshold

    def set_parameters(self, threshold):
        """
        ノイズゲートのしきい値を設定します。
        :param threshold: float
            信号をカットするしきい値
        """
        self.threshold = threshold

    def apply(self, input: np.ndarray) -> np.ndarray:
        """
        ノイズゲートを適用します。
        :param input: np.ndarray
            音声信号（-1.0～1.0）
        :return: np.ndarray
            加工された音声信号
        """
        return np.where(np.abs(input) < self.threshold, 0.0, input)
