import jsonify
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from langsafe.api.models import *
from .logic import *
from ..scanners.input_scanners.input_scanners import LLMFirewall

router = APIRouter(prefix="/v1")
# firewall = LLMFirewall()
@router.get("/health-check")
def get_scan_logs():
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        # 'active_scanners': len(firewall.scanners),
        'service': 'LLM Output Firewall'
    })

# POST /scan
@router.post("/scan", response_model=ScanResponse)
def scan(request: ScanRequest):
    return scan_input_output(request.input, request.output, request.integration_id)

# GET /logs
@router.get("/logs", response_model=LogsResponse)
def get_scan_logs(integration_id: str, status: str, limit: int = 50):
    return get_logs(integration_id, status, limit)

# POST /config/scanners
@router.post("/config/scanners", response_model=ScannerConfigResponse)
def set_scanner_config(request: ScannerConfigRequest):
    return update_scanner_config(request.integration_id, request.scanners)

# GET /scanners
@router.get("/scanners", response_model=ScannersListResponse)
def scanners_list():
    return get_available_scanners()

# WS /ws/events
@router.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    await websocket.accept()
    try:
        while True:
            # Simulate event push
            await websocket.send_json({
                "type": "detection",
                "data": {"log_id": str(uuid.uuid4())}
            })
    except WebSocketDisconnect:
        print("Client disconnected")
