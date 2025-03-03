from fastapi import APIRouter
from loguru import logger
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.WebSocket.manager import manager

router = APIRouter()
@router.websocket("/chat/{room_id}/{user_id}/{nickname}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, user_id: int, nickname: str):
    await manager.connect(websocket, room_id, user_id)
    await manager.broadcast(f"{nickname} (ID: {user_id}) присоединился к чату.", room_id, user_id)
    logger.info("it works here")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{nickname} (ID: {user_id}): {data}", room_id, user_id)
    except WebSocketDisconnect:
        manager.disconnect(room_id, user_id)
        await manager.broadcast(f"{nickname} (ID: {user_id}) покинул чат.", room_id, user_id)