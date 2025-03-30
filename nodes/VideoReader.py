# import os
# import json
# import time
# import logging
from typing import Generator
import cv2

from elements.FrameElement import FrameElement
# from elements.VideoEndBreakElement import VideoEndBreakElement

# logger = logging.getLogger(__name__)


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

            # frame_width = int(cap.get(3))
            # frame_height = int(cap.get(4))
            cv2.imshow('Webcam', frame)

        # Выход из цикла по нажатию клавиши 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
# cv2.waitKey(0)
# cv2.destroyAllWindows()
            yield FrameElement(self.video_source, frame, frame_number)
