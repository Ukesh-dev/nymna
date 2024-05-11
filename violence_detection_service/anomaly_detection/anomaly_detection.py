import os.path
from datetime import datetime
from typing import List

import cv2
from ultralytics import YOLO

from violence_detection_service.anomaly_detection.anamoly_detection_pydantic.send_detected_results_pydantic import \
    AnomalyDetectionVisualize
from violence_detection_service.settings import Settings
from violence_detection_service.anomaly_detection.anamoly_detection_pydantic.anamoly_detection_pdantic import \
    AnomalyDetectionResult, InternalBbox


class AnomalyDetection:

    def __init__(self, source_url: str):
        self.source_url = source_url
        self.model = YOLO("/Users/anishkamukherjee/Documents/nymna/violence_detection_service/model/yolov8s.pt")
        self.cap = cv2.VideoCapture(self.source_url)
        self.id2labels = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.labels2ids = dict((_label, _id) for _id, _label in self.id2labels.items())

    def name2label(self, obj_to_track: List[str]) -> List[int]:
        indices = [self.labels2ids[class_name] for class_name in obj_to_track if class_name in self.labels2ids]
        return indices

    def detect_anomaly(self, conf: float = 0.5) -> list[AnomalyDetectionVisualize] | str:
        detected_anomaly = []
        try:
            for frame in self.get_frames():
                results = self.model(frame)
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        confidence = round(float(box.conf), 2)
                        if confidence >= conf:
                            x1, y1, x2, y2 = list(map(int, box.xyxy[0]))
                            bbox_instance = InternalBbox(
                                top=x1,
                                left=y1,
                                bottom=x2,
                                right=y2
                            )
                            detected_object_index = int(box.cls)
                            class_name = str(self.model.names[detected_object_index])
                            detected_anomaly.append(
                                AnomalyDetectionVisualize(
                                    bbox=[bbox_instance],
                                    score=confidence,
                                    class_name=class_name
                                )
                            )
            return detected_anomaly
        except Exception as e:
            error = f"Error: {e}"
            return error

    def get_frames(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            yield frame

    def get_frame_trims(self, conf: float = 0.5) -> List[AnomalyDetectionResult] | str:
        tracked_objects: List = []
        try:
            frame_count = 0
            for frame in self.get_frames():
                results = self.model(frame, classes=[0], conf=conf)
                for result in results:
                    detections = result.boxes
                    for box in detections:
                        class_id = int(box.cls.item())
                        conf = round(float(box.conf.item()), 2)
                        if conf >= conf:
                            class_name = self.model.names[class_id]
                            if class_name == "person":
                                detected_timestamp = int(datetime.now().timestamp() * 1000)
                                if not os.path.exists(Settings.ABS_TRIMMED_FRAME_PATH):
                                    os.makedirs(Settings.ABS_TRIMMED_FRAME_PATH)
                                x1, y1, x2, y2 = List[map(int, box.xyxy[0])]
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                file_name = f"frame_trimmed_video_{class_name}_{frame_count}.jpg"
                                cv2.imwrite(os.path.join(Settings.ABS_TRIMMED_FRAME_PATH, file_name), frame)
                                print(f"Saved at: {file_name}")
                                cv2.imshow("Frame", frame)
                                key = cv2.waitKey(1) & 0xFF
                                if key == ord("q"):
                                    break
                                cv2.putText(frame, 'OpenCV', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 2,
                                            cv2.LINE_AA)
                                frame_count += 1
                                tracked_objects.append(
                                    AnomalyDetectionResult(
                                        detected_timestamp=detected_timestamp,
                                        source=self.source_url,
                                        class_name=class_name,
                                        confidence=conf
                                    )
                                )
            return tracked_objects
        except Exception as e:
            error = f"Error: {e}"
            return error
