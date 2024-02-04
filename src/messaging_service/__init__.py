import uvicorn

from contextlib import asynccontextmanager
from functools import partial
from fastapi import FastAPI, WebSocket
from sqlmodel import Session, SQLModel, create_engine

from .api import get, websocket_endpoint
from .api.auth import token, read_users_me, read_own_items, User


config = {
    "host": "0.0.0.0",
    "port": 5000,
    "log_level": "info",
    "db": {"URI": "sqlite:///test.db"},
    "auth": {"algorithm": "HS256", "access_token_expire_minutes": 30},
}

connect_args = {"check_same_thread": False}
engine = create_engine(config["db"]["URI"], echo=True, connect_args=connect_args)


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


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
    app.post("/token")(token)
    app.get("/users/me/", response_model=User)(read_users_me)
    app.get("/users/me/items/")(read_own_items)

    manager = ConnectionManager()
    # TODO: Add manager as parameter to websocket_endpoint by using partial
    app.websocket("/ws/{client_id}")(partial(websocket_endpoint, manager=manager))

    uvicorn.run(
        "messaging_service:app",
        host=config.get("host"),
        port=config.get("port"),
        log_level=config.get("log_level"),
    )


if __name__ == "__main__":
    main()
