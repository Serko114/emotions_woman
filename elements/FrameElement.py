import numpy as np
import time


class FrameElement:
    # Класс, содержаций информацию о конкретном кадре видеопотока
    def __init__(
        self,
        source: str,
        frame: np.ndarray,
        frame_num: float,
        frame_result: np.ndarray | None = None,
    ) -> None:
        self.source = source  # Путь к видео или номер камеры с которой берем поток
        self.frame = frame  # Кадр bgr формата
        self.frame_num = frame_num  # Нормер кадра с потока
        self.frame_result = frame_result  # Итоговый обработанный кадр
