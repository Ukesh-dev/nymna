import os.path
from datetime import datetime
from typing import List

import cv2
from ultralytics import YOLO

from violence_detection_service.settings import get_model_path, Settings
from violence_detection_service.anomaly_detection.anamoly_detection_pydantic.anamoly_detection_pdantic import \
    AnomalyDetectionResult


class AnomalyDetection:

    def __init__(self, source_url: str):
        self.source_url = source_url
        self.model = YOLO(get_model_path())
        self.cap = cv2.VideoCapture(source_url)
        self.reverse_dict = {v: k for k, v in self.model.names}
        self.w, self.h, self.fps = self.get_video_properties()

    def get_video_properties(self):
        return (int(self.cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

    def get_trackable_objects(self) -> dict[int:str]:
        return self.model.names

    def get_indices(self, obj_to_track: List[str]):
        indices = [self.reverse_dict[class_name] for class_name in obj_to_track if class_name in self.reverse_dict]
        return indices

    def detect_anomaly(self, frame, conf: float = 0.5) -> List[AnomalyDetectionResult] | str:
        results = self.model(frame)
        tracked_objects: List = []
        try:
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    confidence = round(float(box.conf), 2)
                    if confidence >= conf:
                        detected_object_index = int(box.cls)
                        class_name = str(self.model.names[detected_object_index])
                        if class_name == "person":
                            start_timestamp: int = int(datetime.now().timestamp() * 1000)
                            frame_directory = Settings.ABS_TRIMMED_FRAME_DIR
                            if not os.path.exists(frame_directory):
                                os.makedirs(frame_directory)
                            tracked_objects.append(
                                AnomalyDetectionResult(
                                    start_timestamp=start_timestamp,
                                    source=self.source_url,
                                    class_name=class_name,
                                    confidence=confidence
                                )
                            )
            return tracked_objects
        except Exception as e:
            error = f"Error: {e}"
            return error
