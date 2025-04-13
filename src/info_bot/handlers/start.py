import asyncio
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.fsm.state import State

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import aiohttp
import re
from handlers.main_menu import show_main_menu
from handlers.onboarding import choice_onboarding
from states import RegistrationStates, LKStates
from texts.error import UserAlreadyRegistered, ErrorAuth, NotValueForAuth
from texts.start import Start

from config import settings

import logging

logger = logging.getLogger(__name__)


router = Router()


def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


async def del_msg(message: types.Message, msgs: list[types.Message]):
    await message.bot.delete_messages(message.chat.id, msgs)


async def auth_user(user_data, chat_id: str):
    email = user_data.get("email")
    persinal_number = user_data.get("personal_number")

    if email == None or persinal_number == None or chat_id == None:
        raise NotValueForAuth()

    headers = {"Authorization": f"Basic {settings.AUTH_CORE_SERVER}"}

    body = {
        "email": email,
        "personalNumber": persinal_number,
        "chatId": str(chat_id),
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{settings.URL_CORE_SERVER}/core/students/auth",
                json=body,
                headers=headers) as response:
            if response.status < 400:
                response_data = await response.json()
                return response_data.get("id")
            elif response.status == 423:
                raise UserAlreadyRegistered()
            else:
                raise ErrorAuth()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()

    user_data = await state.get_data()
    if user_data.get("user_id") != None:
        await choice_onboarding(message, state)

    await state.set_state(RegistrationStates.WAITING_FOR_EMAIL)

    welcome_msg = await message.answer(Start.hellow())

    await state.update_data(start_message_del=[welcome_msg.message_id])


@router.message(RegistrationStates.WAITING_FOR_EMAIL)
async def process_email(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    list_del_msg = user_data.get("start_message_del")

    if is_valid_email(message.text):
        await state.update_data(email=message.text)

        await state.set_state(RegistrationStates.WAITING_FOR_STUDENT_ID)

        msg = await message.answer(Start.input_number_student())
        list_del_msg.append(message.message_id)
        list_del_msg.append(msg.message_id)

        await state.update_data(start_message_del=list_del_msg)

    else:
        msg = await message.answer(Start.incorrect_format_email())
        await asyncio.sleep(5)
        await del_msg(message, [msg.message_id, message.message_id])


@router.message(RegistrationStates.WAITING_FOR_STUDENT_ID)
async def process_student_id(message: types.Message, state: FSMContext):
    await state.update_data(personal_number=message.text)

    user_data = await state.get_data()
    list_del_msg = user_data.get("start_message_del")
    list_del_msg.append(message.message_id)

    try:
        user_id = await auth_user(user_data, message.chat.id)
        await state.update_data(user_id=user_id)
        await choice_onboarding(message, state)
        await del_msg(message, list_del_msg)
        await state.update_data(start_message_del=[])

    except UserAlreadyRegistered as error_user:
        msg = await message.answer(Start.person_in_account())
        await asyncio.sleep(5)
        list_del_msg.append(msg.message_id)
        await del_msg(message, list_del_msg)

        await state.set_state(RegistrationStates.WAITING_FOR_EMAIL)
        msg2 = await message.answer(Start.second_input())
        await state.update_data(start_message_del=[msg2.message_id])

    except ErrorAuth as error_auth:
        await del_msg(message, list_del_msg)

        await state.set_state(RegistrationStates.WAITING_FOR_EMAIL)
        msg = await message.answer(Start.second_input())
        await state.update_data(start_message_del=[msg.message_id])

    except NotValueForAuth as not_val:
        pass
