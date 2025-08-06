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

def scan_input_output(input_text: str, output_text: str, integration_id: str,firewall):


    try:
        sanitized_prompt, is_valid, results = firewall.scan_prompt(input_text)

        return {
            'original_prompt': input_text,
            'sanitized_prompt': sanitized_prompt,
            'is_valid': is_valid,
            'risk_score': results['total_risk_score'],
            'processing_time_ms': results['total_processing_time'] * 1000,
            'active_scanners': results['active_scanners'],
            'scanner_results': results['scanner_results']
        }
    except Exception as e:
        return {'error': f'Scanning failed: {str(e)}'}, 500

def get_logs(integration_id: str, status: str, limit: int):
    logs = [log for log in LOGS_DB if log["integration_id"] == integration_id and log["status"] == status]
    return {"logs": logs[:limit], "total": len(logs)}

def update_scanner_config(integration_id: str, scanners: dict):
    for name, conf in scanners.items():
        SCANNER_CONFIGS[name] = conf
    return {"status": "updated", "affected": len(scanners)}

def get_available_scanners():
    return SCANNERS
