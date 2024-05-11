import os


def get_model_path():
    root_path = os.getcwd()
    abs_model_path = os.path.join(root_path, 'model/yolov8s.pt')
    return abs_model_path


def get_yaml_path():
    root_path = os.getcwd()
    abs_yaml_path = os.path.join(root_path, 'yaml/custom_data.yaml')
    return abs_yaml_path


def get_video_path():
    abs_video_path = os.path.join(os.getcwd(), "videos/person4.mp4")
    return abs_video_path


class Settings:
    ABS_TRIMMED_FRAME_DIR = "/Users/anishkamukherjee/Documents/nymna/violence_detection_service/trimmed_frame"
    ABS_TRIMMED_FRAME_PATH = "/Users/anishkamukherjee/Documents/nymna/violence_detection_service/trimmed_frames"
