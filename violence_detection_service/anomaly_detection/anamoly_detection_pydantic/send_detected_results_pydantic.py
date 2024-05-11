from typing import List

from pydantic import BaseModel

from violence_detection_service.anomaly_detection.anamoly_detection_pydantic.anamoly_detection_pdantic import \
    InternalBbox


class AnomalyDetectionVisualize(BaseModel):
    bbox: List[InternalBbox] = []
    class_name: str = ''
    confidence: float = 0
