from fastapi import WebSocket, WebSocketDisconnect

from ...exceptions import JWTError

async def websocket_auth(websocket: WebSocket, auth):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        return None

    try:
        user_id = auth.get_user_from_token(token)
        return user_id
    except JWTError:
        await websocket.close(code=1008)
        return None