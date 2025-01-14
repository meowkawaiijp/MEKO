import numpy as np
import scipy.signal as signal

class FourierNoiseCanceller:
    def __init__(self, noise_threshold=0.05, noise_reduction_factor=0.8, frame_size=2048, hop_size=1024, fs=44100):
        """
        フーリエ変換を使ったノイズキャンセリング
        :param noise_threshold: ノイズとみなす音声信号の閾値
        :param noise_reduction_factor: ノイズを削減する割合
        :param frame_size: フレームサイズ（STFTのサイズ）
        :param hop_size: ホップサイズ（STFTのシフトサイズ）
        :param fs: サンプリングレート（Hz）
        """
        self.noise_threshold = noise_threshold
        self.noise_reduction_factor = noise_reduction_factor
        self.frame_size = frame_size
        self.hop_size = min(frame_size // 2, hop_size)  # hop_sizeをframe_sizeの半分以下に設定
        self.fs = fs
        self.background_noise_spectrum = None

    def set_parameters(self, noise_threshold, noise_reduction_factor):
        """
        ノイズキャンセリングのパラメータを設定
        :param noise_threshold: ノイズとみなす音声信号の閾値
        :param noise_reduction_factor: ノイズを削減する割合
        """
        self.noise_threshold = noise_threshold
        self.noise_reduction_factor = noise_reduction_factor

    def estimate_background_noise(self, input: np.ndarray):
        """
        入力信号から背景ノイズのスペクトルを推定
        :param input: np.ndarray 音声信号
        """
        # STFTを計算
        _, _, Zxx = signal.stft(input, fs=self.fs, nperseg=self.frame_size, noverlap=self.hop_size)
        # ノイズとみなす部分を抽出し、背景ノイズのスペクトルを推定
        noise_mask = np.abs(Zxx) < self.noise_threshold
        self.background_noise_spectrum = np.mean(np.abs(Zxx[noise_mask]), axis=1) if np.any(noise_mask) else 0

    def apply(self, input: np.ndarray) -> np.ndarray:
        """
        ノイズキャンセリングを適用する
        :param input: np.ndarray 音声信号
        :return: np.ndarray 加工された音声信号
        """
        # 背景ノイズを推定する（初回または更新時のみ）
        if self.background_noise_spectrum is None:
            self.estimate_background_noise(input)

        # STFTを計算
        _, _, Zxx = signal.stft(input, fs=self.fs, nperseg=self.frame_size, noverlap=self.hop_size)

        # 背景ノイズスペクトルを減衰させる
        Zxx_cleaned = Zxx - self.background_noise_spectrum[:, None]
        Zxx_cleaned = np.clip(Zxx_cleaned, 0, None)  # 負の値を除去

        # 逆STFTで信号を再構成
        _, cleaned_signal = signal.istft(Zxx_cleaned, fs=self.fs, nperseg=self.frame_size, noverlap=self.hop_size)

        return np.clip(cleaned_signal, -1.0, 1.0)
