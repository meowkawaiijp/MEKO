import numpy as np

class Compressor:
    def __init__(self, threshold=0.5, ratio=4.0):
        self.threshold = threshold
        self.ratio = ratio

    def set_parameters(self, threshold, ratio):
        """
        コンプレッサーのパラメータを設定する
        :param threshold: float
            圧縮が適用される閾値
        :param ratio: float
            圧縮の比率
        """
        self.threshold = threshold
        self.ratio = ratio

    def apply(self, input: np.ndarray) -> np.ndarray:
        """
        コンプレッサーエフェクトを適用する
        :param input: np.ndarray
            音声信号
        :return: np.ndarray
            加工された音声信号
        """
        output = np.copy(input)
        output[np.abs(input) > self.threshold] = self.threshold + (output[np.abs(input) > self.threshold] - self.threshold) / self.ratio
        return output
