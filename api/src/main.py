import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings

from routers.chat import router as r_chat

from telegram.core_userbot import core_user_bot

_log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _log.info("Start server")
    await core_user_bot.connect()

    yield

    await core_user_bot.disconnect()
    _log.info("Stop server")


app = FastAPI(
    lifespan=lifespan,
    root_path="/api"
)

origins = [
    settings.LIST_CORS
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(r_chat)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
