from scipy.signal import butter, lfilter
import numpy as np
class Equalizer:
    def __init__(self, lowcut=100.0, highcut=1000.0, fs=44100, order=5):
        self.lowcut = lowcut
        self.highcut = highcut
        self.fs = fs
        self.order = order

    def set_parameters(self, lowcut, highcut, fs):
        """
        イコライザーのパラメータを設定する
        :param lowcut: float
            最低周波数（Hz）
        :param highcut: float
            最高周波数（Hz）
        :param fs: float
            サンプリング周波数
        """
        self.lowcut = lowcut
        self.highcut = highcut
        self.fs = fs

    def butter_bandpass(self):
        nyquist = 0.5 * self.fs
        low = self.lowcut / nyquist
        high = self.highcut / nyquist
        b, a = butter(self.order, [low, high], btype='band')
        return b, a

    def apply(self, input: np.ndarray) -> np.ndarray:
        """
        バンドパスフィルターを適用してイコライザー効果を作成する
        :param input: np.ndarray
            音声信号
        :return: np.ndarray
            加工された音声信号
        """
        b, a = self.butter_bandpass()
        return lfilter(b, a, input)
