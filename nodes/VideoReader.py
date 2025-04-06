from typing import Generator
import cv2
from elements.FrameElement import FrameElement
import numpy as np


class VideoReader:
    """Модуль для чтения кадров с видеопотока"""

    def __init__(self, config: dict) -> None:
        self.video_pth = config["src"]
        self.video_source = f"Processing of {self.video_pth}"
        self.stream = cv2.VideoCapture(self.video_pth)

    def process(self) -> Generator[FrameElement, None, None]:
        # номер кадра текущего видео
        frame_number = 0
        while True:
            ret, frame = self.stream.read()
            frame_number += 1
# ------------------------блок 'для просмотра видео'------
            # cv2.imshow('Webcam', frame)
            # # Выход из цикла по нажатию клавиши 'q'
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            # cv2.waitKey(1)
# -----------------------конец блока 'для просмотра видео'------
            yield FrameElement(self.video_source, frame, frame_number)
