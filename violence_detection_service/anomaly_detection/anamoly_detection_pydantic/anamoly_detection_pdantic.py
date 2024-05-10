from pydantic import BaseModel


class AnomalyDetectionResult(BaseModel):
    detected_timestamp: int = 0
    end_timestamp: int = 0
    source: str = ''
    class_name: str = ''
    # location: str = ''
    confidence: float = 0.0
