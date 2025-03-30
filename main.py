import hydra
from nodes.VideoReader import VideoReader
import cv2


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(config) -> None:
    video_reader = VideoReader(config["video_reader"])

    for frame_element in video_reader.process():
        print('iiiiiiiiii')
        print()


if __name__ == "__main__":
    main()
