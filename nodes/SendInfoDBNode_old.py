import time
import logging
import psycopg2
import numpy as np

from elements.FrameElement import FrameElement
from elements.VideoEndBreakElement import VideoEndBreakElement
from utils_local.utils import profile_time

logger = logging.getLogger(__name__)


class SendInfoDBNode:
    """Модуль для отправки актуальной информации о трафике в базу данных"""

    def __init__(self, config: dict) -> None:
        config_db = config["send_info_db_node"]
        self.drop_table = config_db["drop_table"]
        self.how_often_add_info = config_db["how_often_add_info"]
        self.table_name = config_db["table_name"]
        # self.last_db_update = time.time()
        print('--------------------------------------')
        # Параметры подключения к базе данных
        db_connection = config_db["connection_info"]
        conn_params = {
            "user": db_connection["user"],
            "password": db_connection["password"],
            "host": db_connection["host"],
            "port": str(db_connection["port"]),
            "database": db_connection["database"],
        }
        print(conn_params)
        # print('--------------------------------------')
        # self.buffer_analytics_sec = (
        #     config["general"]["buffer_analytics"] * 60
        #     + config["general"]["min_time_life_track"]
        # )  # столько по времени буфер набирается и информацию о статистеке выводить рано

        # Подключение к базе данных
        try:
            self.connection = psycopg2.connect(**conn_params)
            print("Connected to PostgreSQL")
            print('--------------------------------------')
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)

        # Создание курсора для выполнения SQL-запросов
        self.cursor = self.connection.cursor()

        # SQL-запрос для удаления таблицы, если она уже существует
        drop_table_query = f"DROP TABLE IF EXISTS {self.table_name};"

        if self.drop_table:
            # Удаление таблицы, если она уже существует
            try:
                self.cursor.execute(drop_table_query)
                self.connection.commit()
                logger.info(f"The table has been deleted")
            except (Exception, psycopg2.Error) as error:
                logger.error(f"Error while dropping table:: {error}")

        # SQL-запрос для создания таблицы
        # create_table_query = f"""
        #     CREATE TABLE IF NOT EXISTS {self.table_name} (
        #     id SERIAL PRIMARY KEY,
        #     timestamp INTEGER,
        #     timestamp_date TIMESTAMP,
        #     cars INTEGER,
        #     road_1 FLOAT,
        #     road_2 FLOAT,
        #     road_3 FLOAT,
        #     road_4 FLOAT,
        #     road_5 FLOAT
        # );
        # """
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            id SERIAL PRIMARY KEY,
            track_id INTEGER,
            Xmin INT,
            Ymin INT,
            Xmax INT,
            Ymax INT);"""
        #     class VARCHAR(12),
        #     calm INT,
        #     joyful INT,
        #     delighted INT,
        #     surprised INT,
        #     sad INT
        #     evil INT
        #     conf FLOAT(4)
        # );
        # """

        # Создание таблицы
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            logger.info(f"СОЗДАНИЕ ТАБЛИЦЫ {self.table_name} ЗАВЕРШЕНО УДАЧНО")
            print('--------------------------------------')
        except (Exception, psycopg2.Error) as error:
            logger.error(f"Error while creating table: {error}")

    # @profile_time
    def process(self, frame_element: FrameElement) -> FrameElement:
        # Выйти из обработки если это пришел VideoEndBreakElement а не FrameElement
        if isinstance(frame_element, VideoEndBreakElement):
            return frame_element
        assert isinstance(
            frame_element, FrameElement
        ), f"SendInfoDBNode | Неправильный формат входного элемента {type(frame_element)}"

        # Получение значений для записи в бд новой строки:
        # info_dictionary = frame_element.info
        # timestamp = frame_element.timestamp
        # timestamp_date = frame_element.timestamp_date

        id_list = frame_element.id_list  # вид [1]
        bboxes = frame_element.tracked_xyxy  # вид [[280, 65, 430, 289]]
        # id_list = '{' + ','.join(map(str, np.array(id_list).flatten())) + '}'
        # bboxes = '{' + ','.join(map(str, np.array(bboxes).flatten())) + '}'
# данные, которые нужно занести в таблицу: [1]  [[280, 65, 430, 289]] ['sad'] [0 0 0 0 1 0] [0.9110729694366455]
        # Проверка, нужно ли отправлять информацию в базу данных
        # current_time = time.time()
        # if current_time - self.last_db_update >= self.how_often_add_info:
        #     self._insert_in_db(info_dictionary, timestamp, timestamp_date)
        # frame_element.send_info_of_frame_to_db = True
        # self.last_db_update = (
        #     current_time  # Обновление времени последнего обновления базы данных
        # )
        self._insert_in_db(id_list, bboxes)

        return frame_element

    def _insert_in_db(
        self, id_list: list, bboxes: list  # timestamp: float, timestamp_date: float
    ) -> None:
        # Формирование и выполнение SQL-запроса для вставки данных в бд
        insert_query = (
            f"INSERT INTO {self.table_name} "
            # , class, calm, joyful, delighted, surprised, sad, evil, conf) "
            "(            track_id, Xmin, Ymin, Xmax, Ymax)"
            "VALUES (%s, %s, %s, %s, %s);"  # , %s, %s, %s);"
        )
        try:
            self.cursor.execute(
                insert_query,
                (
                    int(id_list[0]),
                    int(bboxes[0][0]),
                    int(bboxes[0][1]),
                    int(bboxes[0][2]),
                    int(bboxes[0][3])
                    # frame_element.tracked_xyxy,
                    # info_dictionary["cars_amount"],
                    # (
                    #     info_dictionary["roads_activity"][1]
                    #     if timestamp >= self.buffer_analytics_sec
                    #     else None
                    # ),
                    # (
                    #     info_dictionary["roads_activity"][2]
                    #     if timestamp >= self.buffer_analytics_sec
                    #     else None
                    # ),
                    # (
                    #     info_dictionary["roads_activity"][3]
                    #     if timestamp >= self.buffer_analytics_sec
                    #     else None
                    # ),
                    # (
                    #     info_dictionary["roads_activity"][4]
                    #     if timestamp >= self.buffer_analytics_sec
                    #     else None
                    # ),
                    # (
                    #     info_dictionary["roads_activity"][5]
                    #     if timestamp >= self.buffer_analytics_sec
                    #     else None
                    # ),
                ),
            )
            self.connection.commit()
            logger.info(f"Successfully inserted data into PostgreSQL")
        except (Exception, psycopg2.Error) as error:
            logger.error(
                f"Error while inserting data into PostgreSQL: {error}")
