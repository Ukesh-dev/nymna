from typing import List

from pydantic import BaseModel


class InternalBbox(BaseModel):
    top: int = 0
    left: int = 0
    bottom: int = 0
    right: int = 0


class AnomalyDetectionResult(BaseModel):
    detected_timestamp: int = 0
    source: str = ''
    class_name: str = ''
    confidence: float = 0.0
