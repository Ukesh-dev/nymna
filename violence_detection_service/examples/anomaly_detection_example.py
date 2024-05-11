from violence_detection_service.anomaly_detection.anomaly_detection import AnomalyDetection

if __name__ == '__main__':
    source_url = "http://127.0.0.1:8000/video"
    anomaly_detection = AnomalyDetection(source_url)
    anomaly_detection.get_frame_trims(conf=0.5)

