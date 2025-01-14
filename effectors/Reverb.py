import numpy as np
class Reverb:
    def __init__(self, reverb_amount=0.5):
        self.reverb_amount = reverb_amount

    def set_parameters(self, reverb_amount):
        """
        リバーブのパラメータを設定する
        :param reverb_amount: float
            リバーブの強度
        """
        self.reverb_amount = reverb_amount

    def apply(self, input: np.ndarray) -> np.ndarray:
        """
        リバーブエフェクトを適用する
        :param input: np.ndarray
            音声信号
        :return: np.ndarray
            加工された音声信号
        """
        reverb_signal = np.zeros_like(input)
        for i in range(1, len(input)):
            reverb_signal[i] = input[i] + self.reverb_amount * input[i - 1]
        return reverb_signal
