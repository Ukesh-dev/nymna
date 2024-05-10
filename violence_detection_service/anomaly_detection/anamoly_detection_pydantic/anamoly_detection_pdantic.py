from pydantic import BaseModel


class AnomalyDetectionResult(BaseModel):
    timestamp: int = 0
    source: str = ''
    class_name: str = ''
    # location: str = ''
    confidence: float = 0.0
