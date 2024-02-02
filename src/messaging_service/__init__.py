import uvicorn

from functools import partial
from fastapi import FastAPI, WebSocket

from .api import get, websocket_endpoint


app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


def main():

    app.get("/")(get)

    manager = ConnectionManager()
    # TODO: Add manager as parameter to websocket_endpoint by using partial
    app.websocket("/ws/{client_id}")(partial(websocket_endpoint, manager=manager))

    uvicorn.run("messaging_service:app", host="0.0.0.0", port=5000, log_level="info")


if __name__ == "__main__":
    main()
