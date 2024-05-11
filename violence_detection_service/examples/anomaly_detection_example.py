from violence_detection_service.anomaly_detection.anomaly_detection import AnomalyDetection

if __name__ == '__main__':
    source_url = "/Users/anishkamukherjee/Documents/nymna/violence_detection_service/videos/6secvideo.mp4"
    anomaly_detection = AnomalyDetection(source_url, classes=["person"], conf=0.5)
    anomaly_detection.visualize_anomalies()
