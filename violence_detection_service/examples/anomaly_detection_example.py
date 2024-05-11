<<<<<<< HEAD
=======
import random

>>>>>>> 15dda5fc54ae47dfc1ea5cd92631e85e74ac6742
import cv2

from violence_detection_service.anomaly_detection.anomaly_detection import AnomalyDetection

<<<<<<< HEAD
if __name__ == '__main__':
    source_url = "/Users/anishkamukherjee/Documents/nymna/violence_detection_service/videos/person4.mp4"
    anomaly_detection = AnomalyDetection(source_url)
    anomaly_detection.get_frame_trims(conf=0.5)
=======

if __name__ == '__main__':
    video_url = ""
    anomaly_detection = AnomalyDetection(video_url)

    cap = cv2.VideoCapture(video_url)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = anomaly_detection.detect_anomaly(frame)
        if not results:
            print("No anomalies detected")
        # for result in results:
>>>>>>> 15dda5fc54ae47dfc1ea5cd92631e85e74ac6742
