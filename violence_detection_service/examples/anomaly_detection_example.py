from violence_detection_service.anomaly_detection.anomaly_detection import AnomalyDetection

if __name__ == '__main__':
    source_url = "/Users/anishkamukherjee/Documents/nymna/violence_detection_service/videos/person4.mp4"
    anomaly_detection = AnomalyDetection(source_url)
    anomaly_detection.get_frame_trims(conf=0.5)

