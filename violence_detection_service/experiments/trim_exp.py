import os
import random

from ultralytics import YOLO
import cv2

from violence_detection_service.settings import get_model_path, get_video_path

model = YOLO("/Users/anishkamukherjee/Documents/nymna/violence_detection_service/model/yolov8l.pt")


def test():
    try:
        cap = cv2.VideoCapture("/Users/anishkamukherjee/Documents/nymna/violence_detection_service/videos/person4.mp4")

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            results = model(frame, classes=[0])  # Assuming class_id 0 is 'person'
            for result in results:
                detections = result.boxes
                for box in detections:
                    class_id = int(box.cls.item())
                    conf = round(float(box.conf.item()), 2)
                    class_name = model.names[class_id]
                    print(class_name)
                    if class_name == "person":
                        if not os.path.exists("trimmed_video"):
                            os.makedirs("trimmed_video")
                        cv2.imwrite(f"frame_trimmed_video_{class_name}_{frame_count}.jpg", frame)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    test()
