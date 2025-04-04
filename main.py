import hydra
from nodes.VideoReader import VideoReader
from nodes.DetectionTrackingNodes import DetectionTrackingNodes
import cv2


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(config) -> None:
    video_reader = VideoReader(config["video_reader"])
    detection_node = DetectionTrackingNodes(config)

    for frame_element in video_reader.process():
        frame_element = detection_node.process(frame_element)
        print('iiiiiiiiii')
        print()


if __name__ == "__main__":
    main()
