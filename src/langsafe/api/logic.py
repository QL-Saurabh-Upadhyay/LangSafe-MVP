import uuid
from time import time
from typing import List

# Simulated DB
LOGS_DB = []
SCANNER_CONFIGS = {
    "Toxicity": {"enabled": True},
    "Bias": {"enabled": False}
}

SCANNERS = {
    "prompt": ["Anonymize", "Toxicity"],
    "output": ["Bias", "Toxicity"]
}

def scan_input_output(input_text: str, output_text: str, integration_id: str):
    start = time()

    # Fake detection logic
    risk_score = 10
    detections = []
    applied_scanners = ["Toxicity"]

    # Add to log
    log = {
        "log_id": str(uuid.uuid4()),
        "prompt": "redacted",
        "status": "safe" if risk_score < 50 else "blocked",
        "integration_id": integration_id
    }
    LOGS_DB.append(log)

    return {
        "status": log["status"],
        "risk_score": risk_score,
        "detections": detections,
        "applied_scanners": applied_scanners,
        "timing": {"latency_ms": int((time() - start) * 1000)}
    }

def get_logs(integration_id: str, status: str, limit: int):
    logs = [log for log in LOGS_DB if log["integration_id"] == integration_id and log["status"] == status]
    return {"logs": logs[:limit], "total": len(logs)}

def update_scanner_config(integration_id: str, scanners: dict):
    for name, conf in scanners.items():
        SCANNER_CONFIGS[name] = conf
    return {"status": "updated", "affected": len(scanners)}

def get_available_scanners():
    return SCANNERS
