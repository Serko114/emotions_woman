import time
import logging
import psycopg2

from elements.FrameElement import FrameElement
from elements.VideoEndBreakElement import VideoEndBreakElement
from utils_local.utils import profile_time

logger = logging.getLogger(__name__)


class SendInfoDBNode:
    """Модуль для отправки актуальной информации о трафике в базу данных"""

    def __init__(self, config: dict) -> None:
        config_db = config["send_info_db_node"]
        self.drop_table = config_db["drop_table"]
        # self.how_often_add_info = config_db["how_often_add_info"]
        self.table_name = config_db["table_name"]
        # self.last_db_update = time.time()
        # print('--------------------------------------')
        # Параметры подключения к базе данных
        db_connection = config_db["connection_info"]
        # logger.info("БЕГИИИН")
        conn_params = {
            "user": db_connection["user"],
            "password": db_connection["password"],
            "host": db_connection["host"],
            "port": str(db_connection["port"]),
            "database": db_connection["database"],
        }
        # Подключение к базе данных
        try:
            self.connection = psycopg2.connect(**conn_params)
            print("Удачное подключение к PostgreSQL")
            # print('--------------------------------------')
            # logger.info("ПОДСОООООООООООООЕЕЕЕЕЕЕЕЕЕЕЕДИНИЛЫСЬ")
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
        # print('"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        # logger.info("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            id SERIAL PRIMARY KEY,
            track_id INTEGER,
            X_left INT,
            Y_down INT,
            X_right INT,
            Y_up INT,
            class VARCHAR(12),
            calm INT,
            joyfull INT,
            delighted INT,
            surprised INT,
            sad INT,
            evil INT,
            conf FLOAT(20)
        );
        """
        # logger.info("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        # Создание таблицы
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            logger.info(f"СОЗДАНИЕ ТАБЛИЦЫ {self.table_name} ЗАВЕРШЕНО УДАЧНО")
            # print('--------------------------------------')
        except (Exception, psycopg2.Error) as error:
            logger.error(f"Error while creating table: {error}")
        logger.info(
            "====================================================================================")

    def process(self, frame_element: FrameElement) -> FrameElement:
        id_list = frame_element.id_list
        tracked_xyxy = frame_element.tracked_xyxy
        tracked_cls = frame_element.tracked_cls
        cls_id = frame_element.cls_id
        tracked_conf = frame_element.tracked_conf

        self._insert_in_db(id_list, tracked_xyxy,
                           tracked_cls, cls_id, tracked_conf)
        frame_element.send_info_of_frame_to_db = True

        return frame_element

    def _insert_in_db(self, id_list: list,
                      tracked_xyxy: list,
                      tracked_cls: list,
                      cls_id: list,
                      tracked_conf: list) -> None:
        # logger.info(
        #     type(id_list[0]),
        #     type(tracked_xyxy[0][0]),
        #     type(tracked_xyxy[0][1]),
        #     type(tracked_xyxy[0][2]),
        #     type(tracked_xyxy[0][-1]),
        #     type(tracked_cls[0]),
        #     type(int(cls_id[0])),
        #     type(int(cls_id[1])),
        #     type(int(cls_id[2])),
        #     type(int(cls_id[3])),
        #     type(int(cls_id[4])),
        #     type(int(cls_id[5])),
        #     type(float(tracked_conf[0]))

        # )
        insert_query = (
            f"INSERT INTO {self.table_name} "
            "(track_id, X_left, Y_down, X_right, Y_up, class, calm, joyfull, delighted, surprised, sad, evil, conf) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        )
        try:
            self.cursor.execute(
                insert_query,
                (
                    int(id_list[0]),
                    int(tracked_xyxy[0][0]),
                    int(tracked_xyxy[0][1]),
                    int(tracked_xyxy[0][2]),
                    int(tracked_xyxy[0][-1]),
                    tracked_cls[0],
                    int(cls_id[0]),
                    int(cls_id[1]),
                    int(cls_id[2]),
                    int(cls_id[3]),
                    int(cls_id[4]),
                    int(cls_id[-1]),
                    float(tracked_conf[0])

                ),
            )

            self.connection.commit()
            print(self.cursor.fetchall())
            logger.info(f"Успешное добавление данных в PostgreSQL")
            # logger.info(f"Successfully inserted data into PostgreSQL")
        except (Exception, psycopg2.Error) as error:
            logger.error(
                f"Error while inserting data into PostgreSQL: {error}")
