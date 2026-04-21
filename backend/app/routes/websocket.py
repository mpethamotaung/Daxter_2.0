import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.orchestrator import orchestrator

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    queue: asyncio.Queue = asyncio.Queue(maxsize=50)
    orchestrator.subscribe(queue)
    try:
        while True:
            event = await queue.get()
            await ws.send_text(json.dumps(event, default=str))
    except WebSocketDisconnect:
        pass
    finally:
        orchestrator.unsubscribe(queue)
