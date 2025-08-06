from pydantic import BaseModel
from typing import Dict, List, Optional

class ScanRequest(BaseModel):
    input: Optional[str]
    output: Optional[str]
    integration_id: str

class ScanResponse(BaseModel):
    status: str
    risk_score: int
    detections: List[str]
    applied_scanners: List[str]
    timing: Dict[str, int]

class Log(BaseModel):
    log_id: str
    prompt: str
    status: str

class LogsResponse(BaseModel):
    logs: List[Log]
    total: int

class ScannerConfigRequest(BaseModel):
    integration_id: str
    scanners: Dict[str, Dict[str, bool]]

class ScannerConfigResponse(BaseModel):
    status: str
    affected: int

class ScannersListResponse(BaseModel):
    prompt: List[str]
    output: List[str]

class WebSocketEvent(BaseModel):
    type: str
    data: Dict[str, str]
