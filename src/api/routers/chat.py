from fastapi import APIRouter
from telethon.tl.functions.messages import CreateChatRequest  # type: ignore

from api.schemas.chat import AddChatDTO
from api.telegram.core_userbot import core_user_bot


router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("")
async def create_chat(
    data: AddChatDTO
):
    try:
        # result = await core_user_bot.client(CreateChatRequest(
        #     title=data.name,
        #     users=[(await core_user_bot.client.get_me()).id]
        # ))
        pass
    except:
        return {"status": "error"}

    return {"status": "success"}
