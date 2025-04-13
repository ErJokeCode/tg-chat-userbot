import logging
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatMemberUpdated
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.fsm.storage.redis import RedisStorage

import aiohttp
import asyncio

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # noqa

from config import settings


storage = RedisStorage.from_url(settings.URL_REDIS)

bot = Bot(token=settings.TG_TOKEN_CHAT_BOT)
dp = Dispatcher(storage=storage)

_log = logging.getLogger(__name__)


@dp.message(Command("add_group"), F.chat.type.in_({"group", "supergroup"}) & F.from_user.id == 1362536052)
async def all_message_in_group(message: types.Message, state: FSMContext):
    full_name_course = " ".join(message.text.split()[1:])
    link = await message.bot.export_chat_invite_link(message.chat.id)

    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Basic {settings.AUTH_CORE_SERVER}"}
        async with session.post(
            f"{settings.URL_CORE_SERVER}/parser/subject/add_group_tg",
            headers=headers,
            params={"full_name": full_name_course, "link": link}
        ) as resp:
            if resp.status == 200:
                await message.answer(f"Группа успешно добавлена")


@dp.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def all_message_in_group(event: ChatMemberUpdated, state: FSMContext):
    await event.answer("Отправить данные на сервер")


@dp.message(Command("start"), F.chat.type.in_({"private"}))
async def cmd_start(message: types.Message, state: FSMContext):
    # await state.clear()
    user_data = await state.get_data()
    user_id = user_data.get("user_id")
    if user_id == None:
        await message.answer("Зарегестрируйтесть в боте @test123show_bot")
    else:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Basic {settings.AUTH_CORE_SERVER}"}

            # async with session.put(f"{URL_CORE}/core/student/addChat/{user_id}", headers=headers, json={"chatId": str(message.chat.id)}) as resp:
            await message.answer("Какой вопрос вас интенресует")


@dp.message(F.chat.type.in_({"private"}))
async def all_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = user_data.get("user_id")
    if user_id == None:
        await message.answer("Войдите в аккаунт в @test123show_bot")
    else:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Basic {settings.AUTH_CORE_SERVER}"}

            async with session.get(f"{settings.URL_CORE_SERVER}/core/admins", headers=headers) as response_admins:
                if response_admins.status == 200:
                    with aiohttp.MultipartWriter('form-data') as mpwriter:
                        part = mpwriter.append_json(
                            {"content": message.text, "studentId": user_id})
                        part.set_content_disposition('form-data', name="body")

                        async with session.post(f"{settings.URL_CORE_SERVER}/core/chats/from-student", headers=headers, data=mpwriter) as resp:
                            if resp.status == 200:
                                msg = await message.answer("Сообщение отправлено, ожидайте ответа")
                                await asyncio.sleep(5)
                                await msg.delete()
                            else:
                                msg = await message.answer("Неполучилось доставить сообщение куратору, попробуй ещё раз")
                                await asyncio.sleep(5)
                                await msg.delete()

                else:
                    msg = await message.answer("Неполучилось доставить сообщение куратору, попробуй ещё раз")
                    await asyncio.sleep(5)
                    await msg.delete()


async def main():
    _log.info("Start chat bot")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
