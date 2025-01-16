import numpy as np
from scipy.signal import butter, lfilter

class Distortion:
    def __init__(self, drive=10, intensity=1.0, cutoff_freq=8000, fs=44100, apply_lowpass=True, release_factor=0.85):
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
        :param release_factor: float
            エンベロープのリリースファクター（0～1、1に近いと減衰が遅くなる）
        """
        self.drive = drive
        self.intensity = intensity
        self.cutoff_freq = cutoff_freq
        self.fs = fs
        self.apply_lowpass = apply_lowpass
        self.release_factor = release_factor

    def set_parameters(self, drive, intensity, cutoff_freq=None, release_factor=None):
        """
        パラメータを設定
        """
        self.drive = drive
        self.intensity = intensity
        if cutoff_freq is not None:
            self.cutoff_freq = cutoff_freq
        if release_factor is not None:
            self.release_factor = release_factor

    def lowpass_filter(self, signal):
        """
        ローパスフィルタを適用
        """
        nyquist = 0.5 * self.fs
        normal_cutoff = self.cutoff_freq / nyquist
        b, a = butter(4, normal_cutoff, btype='low', analog=False)  # フィルタ次数を4に変更
        return lfilter(b, a, signal)

    def apply_envelope(self, signal):
        """
        エンベロープを適用して減衰を早める
        """
        envelope = np.exp(-np.arange(len(signal)) * (1 - self.release_factor) / len(signal))
        return signal * envelope

    def apply(self, input_signal: np.ndarray) -> np.ndarray:
        """
        ディストーションを適用
        """
        if input_signal.ndim > 1:
            raise ValueError("入力信号は1次元配列である必要があります")

        # 入力信号の正規化
        input_signal = np.clip(input_signal, -1.0, 1.0)  # -1.0～1.0にクリップ

        # 増幅
        amplified = input_signal * self.drive
        amplified = np.clip(amplified, -1.0, 1.0)  # 増幅後にクリップして音量が大きくなりすぎないように

        # ソフトクリッピング
        distorted = np.tanh(amplified * self.intensity)

        # ローパスフィルタを適用（オプション）
        if self.apply_lowpass:
            distorted = self.lowpass_filter(distorted)

        # エンベロープを適用
        distorted = self.apply_envelope(distorted)

        # 出力信号の振幅を調整してクリッピング
        output = distorted / np.max(np.abs(distorted)) if np.max(np.abs(distorted)) > 0 else distorted
        
        # 音量を1/100に減少
        #output = output / 100.0

        return np.clip(output, -1.0, 1.0)  # 最終的に-1.0～1.0にクリップ
