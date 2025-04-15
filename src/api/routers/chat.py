from asyncio import sleep
import logging
from fastapi import APIRouter, HTTPException
from telethon.tl.functions.messages import CreateChatRequest, ExportChatInviteRequest  # type: ignore

from api.schemas.chat import AddChatDTO
from api.telegram.core_userbot import core_user_bot
from api.telegram.core_bot import core_info_bot

_log = logging.getLogger(__name__)


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
        #     users=[
        #         (await core_user_bot.client.get_me()).id,
        #         (await core_info_bot.bot.me()).id
        #     ]
        # ))

        # _log.info("Chat result %s", result)

        # await sleep(5)

        # chat_id = int(result.updates.chats[0].id)
        chat_id = 4761979812

        _log.info("Chat created %s", chat_id)

        chat = await core_user_bot.client.get_entity(chat_id)
        invite = await core_user_bot.client(ExportChatInviteRequest(chat))

        _log.info("Invite %s", invite)

        for user_id in data.users:
            await core_info_bot.bot.send_message(
                chat_id=user_id,
                text=f'Чат {data.name} создан. \n\nСсылка на чат: \n{invite.link}'
            )
    except Exception as e:
        _log.error(e)
        raise HTTPException(status_code=500, detail="Error create chat")

    return {"status": "success"}
