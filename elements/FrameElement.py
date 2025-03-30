import numpy as np
import time


class FrameElement:
    # Класс, содержаций информацию о конкретном кадре видеопотока
    def __init__(
        self,
        source: str,
        frame: np.ndarray,
        timestamp: float,
        frame_num: float,
        roads_info: dict,
        frame_result: np.ndarray | None = None,
        detected_conf: list | None = None,
        detected_cls: list | None = None,
        detected_xyxy: list[list] | None = None,
        tracked_conf: list | None = None,
        tracked_cls: list | None = None,
        tracked_xyxy: list[list] | None = None,
        id_list: list | None = None,
        buffer_tracks: dict | None = None,
    ) -> None:
        self.source = source  # Путь к видео или номер камеры с которой берем поток
        self.frame = frame  # Кадр bgr формата
        # Значение времени с начала потока (в секундах)
        # self.timestamp = timestamp
        self.frame_num = frame_num  # Нормер кадра с потока
        # Словарь с координатми дорог, примыкающих к участку кругового движения
        # self.roads_info = roads_info
        self.frame_result = frame_result  # Итоговый обработанный кадр
        # Время в момент обработки кадра unix формат (в секундах)
        # self.timestamp_date = time.time()
        # Результаты на выходе с YOLO:
        # Список уверенностей задетектированных объектов
        self.detected_conf = detected_conf
        self.detected_cls = detected_cls  # Список классов задетектированных объектов
        self.detected_xyxy = detected_xyxy  # Список списков с координатами xyxy боксов
        # Результаты корректировки трекинг алгоритмом:
        self.tracked_conf = tracked_conf  # Список уверенностей задетектированных объектов
        self.tracked_cls = tracked_cls  # Список классов задетектированных объектов
        self.tracked_xyxy = tracked_xyxy  # Список списков с координатами xyxy боксов
        self.id_list = id_list  # Список обнаруженных id трекуемых объектов
        # Постобработка кадра:
        # Буфер актуальных треков за выбранное время анализа
        # self.buffer_tracks = buffer_tracks
        # Словарь с результирующей статистикой (загруженность дорог + число машин)
        # self.info = {}
        # Флаг того, будет ли с это кадра инфа отправлена в бд
        # self.send_info_of_frame_to_db = False
