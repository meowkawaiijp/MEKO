import numpy as np

class Distortion:
    def __init__(self, drive=10, intensity=1.0):
        self.name = "Distortion"
        self.drive = drive
        self.intensity = intensity

    def set_parameters(self, drive, intensity):
        """
        ドライブ強度と歪みの強さを設定
        :param drive: float
            歪みの強度（大きいほど強い歪み）
        :param intensity: float
            歪みの強さ（1.0を超える値でさらに強い歪みを生成）
        """
        self.drive = drive
        self.intensity = intensity

    def apply(self, input: np.ndarray) -> np.ndarray:
        """
        強い歪みを適用する
        :param input: np.ndarray
            音声信号（np.float32: -1.0～1.0）
        :return: np.ndarray
            加工された音声信号
        """
        amplified = input * self.drive
        distorted = amplified / (1 + np.abs(amplified) ** self.intensity)
        
        output = np.clip(distorted, -1.0, 1.0)
        
        return output
