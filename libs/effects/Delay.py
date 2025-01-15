import numpy as np
class Delay:
    def __init__(self, delay_time=0.5, feedback=0.5, fs=44100):
        self.delay_time = delay_time
        self.feedback = feedback
        self.fs = fs

    def set_parameters(self, delay_time, feedback):
        """
        ディレイのパラメータを設定する
        :param delay_time: float
            ディレイ時間（秒）
        :param feedback: float
            フィードバック量
        """
        self.delay_time = delay_time
        self.feedback = feedback

    def apply(self, input: np.ndarray) -> np.ndarray:
        """
        ディレイエフェクトを適用する
        :param input: np.ndarray
            音声信号
        :return: np.ndarray
            加工された音声信号
        """
        delay_samples = int(self.delay_time * self.fs)
        delayed_signal = np.zeros_like(input)
        for i in range(delay_samples, len(input)):
            delayed_signal[i] = input[i] + self.feedback * delayed_signal[i - delay_samples]
        return delayed_signal
