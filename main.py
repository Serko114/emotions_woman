import hydra
from nodes.VideoReader import VideoReader
import cv2


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(config) -> None:
    video_reader = VideoReader(config["video_reader"])

    # save_video = config["pipeline"]["save_video"]
    # send_info_db = config["pipeline"]["send_info_db"]
    # show_in_web = config["pipeline"]["show_in_web"]

    # if save_video:
    #     video_saver_node = VideoSaverNode(config["video_saver_node"])

    # if send_info_db:
    #     send_info_db_node = SendInfoDBNode(config)

    # if show_in_web:
    #     video_server_node = VideoServer(config)

    for frame_element in video_reader.process():
        print('iiiiiiiiii')
        # frame_element = detection_node.process(frame_element)
        # frame_element = tracker_info_update_node.process(frame_element)
        # frame_element = calc_statistics_node.process(frame_element)

        # if send_info_db:
        #     frame_element = send_info_db_node.process(frame_element)

        # frame_element = show_node.process(frame_element)

        # if save_video:
        #     video_saver_node.process(frame_element)

        # if show_in_web:
        #     if isinstance(frame_element, VideoEndBreakElement):
        #         break  # Обрывание обработки при окончании стрима
        #     video_server_node.update_image(frame_element.frame_result)


if __name__ == "__main__":
    main()
