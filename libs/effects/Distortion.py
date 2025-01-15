import numpy as np
from scipy.signal import butter, lfilter

class Distortion:
    def __init__(self, drive=10, intensity=1.0, cutoff_freq=8000, fs=44100, apply_lowpass=True):
        """
        Distortionクラスの初期化
        :param drive: float
            歪みの強さ（大きいほど強い歪み）
        :param intensity: float
            歪みの非線形性の強さ（1.0以上の値を推奨）
        :param cutoff_freq: float
            ローパスフィルタのカットオフ周波数（Hz）
        :param fs: int
            サンプリング周波数（Hz）
        :param apply_lowpass: bool
            ローパスフィルタを適用するかどうか
        """
        self.drive = drive
        self.intensity = intensity
        self.cutoff_freq = cutoff_freq
        self.fs = fs
        self.apply_lowpass = apply_lowpass

    def set_parameters(self, drive, intensity, cutoff_freq=None):
        """
        パラメータを設定
        :param drive: float
            歪みの強さ
        :param intensity: float
            歪みの非線形性の強さ
        :param cutoff_freq: float or None
            ローパスフィルタのカットオフ周波数（設定しない場合は変更しない）
        """
        self.drive = drive
        self.intensity = intensity
        if cutoff_freq is not None:
            self.cutoff_freq = cutoff_freq

    def lowpass_filter(self, signal):
        """
        ローパスフィルタを適用
        :param signal: np.ndarray
            入力信号
        :return: np.ndarray
            フィルタ適用後の信号
        """
        nyquist = 0.5 * self.fs
        normal_cutoff = self.cutoff_freq / nyquist
        b, a = butter(5, normal_cutoff, btype='low', analog=False)
        return lfilter(b, a, signal)

    def apply(self, input: np.ndarray) -> np.ndarray:
        """
        ディストーションを適用
        :param input: np.ndarray
            音声信号（np.float32: -1.0～1.0）
        :return: np.ndarray
            加工された音声信号
        """
        # 入力信号の正規化
        max_val = np.max(np.abs(input))
        if max_val > 0:
            input = input / max_val

        # 増幅
        amplified = input * self.drive

        # ソフトクリッピング
        distorted = np.tanh(amplified * self.intensity)

        # ローパスフィルタを適用（オプション）
        if self.apply_lowpass:
            distorted = self.lowpass_filter(distorted)

        # 信号の振幅を調整
        output = np.clip(distorted, -1.0, 1.0) * 0.8

        return output