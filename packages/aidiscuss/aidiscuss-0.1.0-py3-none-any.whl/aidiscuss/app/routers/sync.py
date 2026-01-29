"""
WebSocket sync router for real-time data synchronization
Separate from chat streaming WebSocket - dedicated to state sync across tabs/browsers
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from aidiscuss.app.services.broadcast import broadcast_service

router = APIRouter()


@router.websocket("/sync")
async def websocket_sync_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time data synchronization
    Clients connect to this endpoint to receive broadcasts of data changes
    (agent/provider/conversation/settings updates)

    This is separate from the chat streaming WebSocket (/api/chat/stream)
    """
    await broadcast_service.connect(websocket)

    try:
        # Keep connection alive and listen for client messages
        while True:
            data = await websocket.receive_text()

            # Handle keepalive ping/pong
            if data == "ping":
                await websocket.send_text("pong")

    except WebSocketDisconnect:
        broadcast_service.disconnect(websocket)
    except Exception as e:
        print(f"[SyncWebSocket] Error: {e}")
        broadcast_service.disconnect(websocket)
