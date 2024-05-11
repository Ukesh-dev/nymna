import os
from backend.settings import BASE_DIR


def get_model_path():
    root_path = os.getcwd()
    abs_model_path = os.path.join(BASE_DIR, "computervision/model/acc_last.pt")
    return abs_model_path


def get_yaml_path():
    root_path = os.getcwd()
    abs_yaml_path = os.path.join(BASE_DIR, "computervision/yaml/custom_data.yaml")
    return abs_yaml_path


def get_video_path():
    abs_video_path = os.path.join(os.getcwd(), "/videos/person4.mp4")
    return abs_video_path


class Settings:
    ABS_TRIMMED_FRAME_DIR = (
        "/Users/ukeshshrestha/Dev/nymna/backend/computervision/trimmed_frame"
    )
    ABS_TRIMMED_FRAME_PATH = (
        "/Users/ukeshshrestha/Dev/nymna/backend/computervision/trimmed_frames"
    )
