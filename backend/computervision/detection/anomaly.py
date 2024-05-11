from datetime import datetime
from typing import List
import os
import imutils
import cv2
from ultralytics import YOLO

from computervision.settings import Settings, get_model_path
import asyncio
from django.utils.crypto import get_random_string
from backend.settings import BASE_DIR
from channels.layers import get_channel_layer
from core.models import Report
import time
from asgiref.sync import sync_to_async
from core.onesignal import OneSignalNotification

class AnomalyDetection:

    def __init__(self, source_url: str, classes: list[str], conf: float = .5):
        self.classes: List[str] = classes
        self.conf: float = conf
        self.source_url = source_url
        self.model = YOLO(get_model_path())
        self.cap = cv2.VideoCapture(self.source_url)
        self.id2labels = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.labels2ids = {label: idx for idx, label in enumerate(self.id2labels)}
        self.channel_layer = get_channel_layer()

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

    def get_status(self):
        return self.model.names

    def generate_random_folder(self):
        random_folder = "anomaly_" + str(int(time.time()))
        folder_path = os.path.join(BASE_DIR, "static", random_folder)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path, random_folder

    async def notify_clients(self, notitype: str):
        channel_layer = get_channel_layer()
        await self.channel_layer.group_send(
            "notification",
            {
                "type": "send_notification",
                "notification": {
                    "type": notitype,
                    "data": []
                }
            }
        )

    async def get_frame_trims(self) -> list | str:
        tracked_objects: List = []
        timestamp_start = None
        timestamp_end = None
        confidence = 0
        status = "normal"
        folder_path, folder_name = self.generate_random_folder()
        width = self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        height = self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        noti_sent = False
        location = "Kathmandu"
        if "sifal.mp4" in self.source_url:
            location = "Sifal, Kathmandu"
        elif "maitighar.mp4" in self.source_url:
            location = "Maitighar, Kathmandu"

        try:
            frame_count = 0
            skip_frames = 30
            for _ in range(skip_frames):
                self.cap.read()

            await self.notify_clients("first_frame")
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break

                results = self.model.track([frame], persist=True, conf=self.conf)
                for result in results:
                    detections = result.boxes
                    for box in detections:
                        conf = round(float(box.conf.item()), 2)
                        if conf >= self.conf:
                            class_id = int(box.cls.item())
                            class_name = self.model.names[class_id]

                            if class_name == "-fatal-accident-":
                                status = "fatal"
                            elif class_name == "-moderate-accident-" and (status != "fatal" or status is None):
                                status = "moderate"
                            elif class_name == "-normal-accident-" and (status != "fatal" and status != "moderate"):
                                status = "normal"

                            if status == "fatal" and not noti_sent:
                                noti_sent = True
                                OneSignalNotification.send({
                                    "title": "Incident Alert!!!",
                                    "message": f"There has been an fatal accident on {location}"
                                })

                            detect_status = self.get_status()
                            if class_name in detect_status.values():
                                timestamp_end = datetime.now()
                                if not timestamp_start:
                                    timestamp_start = timestamp_end
                                detected_timestamp = int(datetime.now().timestamp() * 1000)
                                x1, y1, x2, y2 = list(map(int, box.xyxy[0]))
                                cv2.rectangle(frame, (x1, y1), (x2, y2),
                                              (0, 0,
                                               255) if class_name == "-fatal-accident-" or class_name == "-moderate-accident-" else (
                                                  0, 255, 0), 2)
                                cv2.putText(frame, f"Status:{status.capitalize()}", (420, 40),
                                            cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                            (0, 255, 0), 1,
                                            cv2.LINE_AA)

                                location_name = "Sifal, Kathmandu"
                                if "maitighar.mp4" in self.source_url:
                                    location_name = "Maitighar, Kathmandu"

                                cv2.putText(frame, location_name, (10, 55), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                            (0, 255, 0), 1,
                                            cv2.LINE_AA)
                                if "maitighar.mp4" not in self.source_url:
                                    cv2.putText(frame, f'{datetime.now().strftime("%Y-%m-%d")}', (10, 25),
                                                cv2.FONT_HERSHEY_DUPLEX, 0.6,
                                                (0, 255, 0), 1,
                                                cv2.LINE_AA)

                                file_name = f"anomaly_{frame_count}_frame.jpg"
                                cv2.imwrite(os.path.join(folder_path, file_name), frame)
                                print(f"Saved at: {file_name}")

                                frame_count += 1
                                tracked_objects.append({
                                    "detected_timestamp": detected_timestamp,
                                    "source": self.source_url,
                                    "class_name": class_name,
                                    "confidence": conf
                                })

                                if conf > confidence:
                                    confidence = conf

                        # Convert the frame to JPEG format
                        ret, buffer = cv2.imencode('.jpg', frame)
                        frame_bytes = buffer.tobytes()

                        # Yield the frame for streaming
                        yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
                        await asyncio.sleep(0.0001)

            # return tracked_objects
            await self.notify_clients("analyze_complete")
        except Exception as e:
            error = f"Error: {e}"
            print(error)
            # return error

        report_creation = sync_to_async(Report.objects.create, thread_sensitive=True)

        source_url = self.source_url
        if "sifal.mp4" in source_url:
            source_url = "http://127.0.0.1:8000/video/sifal"
        elif "maitighar.mp4" in source_url:
            source_url = "http://127.0.0.1:8000/video/maitighar"

        await report_creation(
            source=source_url,
            confidence=confidence,
            status=status,
            timestamp_start=timestamp_start,
            timestamp_end=timestamp_end,
            video=folder_name
        )

        if not noti_sent and status == "moderate":
            # Send Notification
            OneSignalNotification.send({
                "title": "Incident Alert!!!",
                "message": f"There has been an accident on {location}"
            })

        self.cap.release()
