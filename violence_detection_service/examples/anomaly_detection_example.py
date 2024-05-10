import cv2

from violence_detection_service.anomaly_detection.anomaly_detection import AnomalyDetection

if __name__ == '__main__':
    video_url = "/Users/anishkamukherjee/Documents/nymna/violence_detection_service/videos/acc1.mp4"
    anomaly_detection = AnomalyDetection(video_url)

    cap = cv2.VideoCapture(video_url)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = anomaly_detection.detect_anomaly([frame])
        if not results:
            print("No anomalies detected")
        for result in results:
            print(result)
