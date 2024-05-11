import os.path
from datetime import datetime
from typing import List

import cv2
from ultralytics import YOLO

from violence_detection_service.settings import Settings


class AnomalyDetection:

    def __init__(self, source_url: str, classes: list[str], conf: float = .5):
        self.classes: List[str] = classes
        self.conf: float = conf
        self.source_url = source_url
        self.model = YOLO("models/yolov8s.pt")
        self.cap = cv2.VideoCapture(self.source_url)
        self.id2labels = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.labels2ids = {label: idx for idx, label in enumerate(self.id2labels)}

    def name2label(self, obj_to_track: List[str]) -> List[int]:
        indices = [self.labels2ids[class_name] for class_name in obj_to_track if class_name in self.labels2ids]
        return indices

    def detect_anomaly(self) -> list | str:  # raw data
        detected_anomaly = []
        try:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break
                results = self.model(frame, classes=self.name2label(self.classes), conf=self.conf)
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        confidence = round(float(box.conf), 2)
                        if confidence >= self.conf:
                            x1, y1, x2, y2 = list(map(int, box.xyxy[0]))
                            detected_object_index = int(box.cls)
                            class_name = str(self.model.names[detected_object_index])
                            detected_anomaly.append({
                                "bbox": {"top": x1, "left": x2, "bottom": y1, "right": y2},
                                "score": confidence,
                                "class_name": class_name
                            }
                            )
        except Exception as e:
            error = f"Error: {e}"
            return error

        return detected_anomaly

    def get_frames(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            yield frame

    def get_frame_trims(self) -> list | str:
        tracked_objects: List = []
        try:
            frame_count = 0
            while self.cap.isOpened:
                ret, frame = self.cap.read()
                print(f"Frame count {frame_count}")
                if not ret:
                    break
                results = self.model(frame, classes=[0], conf=self.conf)
                for result in results:
                    detections = result.boxes
                    for box in detections:
                        conf = round(float(box.conf.item()), 2)
                        if conf >= self.conf:
                            class_id = int(box.cls.item())
                            class_name = self.model.names[class_id]
                            if class_name == "person":
                                detected_timestamp = int(datetime.now().timestamp() * 1000)
                                if not os.path.exists(Settings.ABS_TRIMMED_FRAME_PATH):
                                    os.makedirs(Settings.ABS_TRIMMED_FRAME_PATH)
                                file_name = f"frame_trimmed_video_{class_name}_{frame_count}.jpg"
                                cv2.imwrite(os.path.join(Settings.ABS_TRIMMED_FRAME_PATH, file_name), frame)
                                print(f"Saved at: {file_name}")
                                # x1, y1, x2, y2 = list(map(int, box.xyxy[0]))
                                # cv2.imshow("Frame", frame)
                                # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                # cv2.putText(frame, 'Frame', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 2,
                                #             cv2.LINE_AA)
                                # if cv2.waitKey(1) & 0xFF == ord('q'):
                                #     break
                                frame_count += 1
                                tracked_objects.append({
                                    "detected_timestamp": detected_timestamp,
                                    "source": self.source_url,
                                    "class_name": class_name,
                                    "confidence": conf
                                })
            return tracked_objects
        except Exception as e:
            error = f"Error: {e}"
            return error

    def visualize_anomalies(self):  # live stream
        try:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break
                results = self.model(frame, classes=[0], conf=self.conf)
                results_ = results[0].plot()
                cv2.imshow("Anomaly Frame", results_)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            self.cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            error = f"Error: {e}"
            return error
