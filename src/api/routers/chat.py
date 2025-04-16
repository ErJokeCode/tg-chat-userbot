from telethon.tl.types import InputPeerUser, InputPeerChat, InputPeerChannel
from asyncio import sleep
import logging
from fastapi import APIRouter, HTTPException
from telethon.tl.functions.messages import CreateChatRequest, ExportChatInviteRequest, AddChatUserRequest, EditChatAdminRequest  # type: ignore
from telethon.tl.types import InputPeerUser, InputPeerChat

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
        result = await core_user_bot.client(CreateChatRequest(
            title=data.name,
            users=[
                (await core_user_bot.client.get_me()).id,
            ]
        ))

        chat_id = result.updates.chats[0].id

        bot_info_id = (await core_info_bot.bot.get_me()).id
        chat, bot = await get_entities_safely(chat_id, bot_info_id)

        # user_chats = await core_user_bot.client.get_dialogs()
        # _log.info("User chats %s", user_chats)

        # chat_users = await core_user_bot.client.get_participants(chat)
        # _log.info("Chat users %s", chat_users)

        await core_user_bot.client(AddChatUserRequest(
            chat_id=chat_id,
            user_id=bot_info_id,
            fwd_limit=0
        ))

        await core_user_bot.client(EditChatAdminRequest(
            chat_id=chat_id,
            user_id=bot_info_id,
            is_admin=True
        ))

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


async def get_entities_safely(chat_id, bot_id):
    try:
        _log.info("Trying to get entities through get_entity")
        chat = await core_user_bot.client.get_entity(chat_id)
        bot = await core_user_bot.client.get_entity(bot_id)
        return chat, bot

    except (ValueError, TypeError) as e:
        _log.warning(
            f"Entity not in cache: {e}. Trying alternative methods...")

        try:
            bot = await core_user_bot.client.get_input_entity(InputPeerUser(user_id=bot_id, access_hash=0))
        except Exception as e:
            _log.error(f"Failed to get bot entity: {e}")
            raise ValueError(f"Could not resolve bot entity: {e}")

        try:
            try:
                chat = InputPeerChat(chat_id=chat_id)
                await core_user_bot.client.get_input_entity(chat)
                return chat, bot
            except:
                try:
                    chat = await core_user_bot.client.get_input_entity(chat_id)
                    return chat, bot
                except:
                    chat = InputPeerUser(user_id=chat_id, access_hash=0)
                    await core_user_bot.client.get_input_entity(chat)
                    return chat, bot

        except Exception as e:
            _log.error(f"Failed to resolve chat: {e}")
            raise ValueError(f"Could not resolve chat entity: {e}")
