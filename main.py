import hydra
from nodes.VideoReader import VideoReader
from nodes.DetectionTrackingNodes import DetectionTrackingNodes
from nodes.VideoShow import VideoShowDetection
from nodes.VideoSaverNode import VideoSaverNode
import cv2


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(config) -> None:
    video_reader = VideoReader(config["video_reader"])
    detection_node = DetectionTrackingNodes(config)
    show_detection_node = VideoShowDetection(config)
    save_video = config["pipeline"]["save_video"]
    video_show = config["pipeline"]["video_show"]
    if video_show:
        show_detection_node = VideoShowDetection(config)
    if save_video:
        video_saver_node = VideoSaverNode(config["video_saver_node"])

    for frame_element in video_reader.process():
        frame_element = detection_node.process(frame_element)
        print('FUCK!')
        # frame_element = show_detection_node.process(frame_element)
        if video_show:
            show_detection_node.process(frame_element)
        if save_video:
            video_saver_node.process(frame_element)
        print('iiiiiiiiii')
        print()


if __name__ == "__main__":
    main()
