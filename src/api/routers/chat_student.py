from io import BytesIO
import tempfile
from aiogram.types.input_file import BufferedInputFile
from aiogram.utils.media_group import MediaGroupBuilder

import os
import shutil
from fastapi import APIRouter, UploadFile

from api.telegram.core_bot import core_chat_bot

router = APIRouter(
    prefix="/chat_student",
    tags=["Chat with student"],
)


@router.post("/{chat_id}/text")
async def chat_student_text(chat_id: str, text: str):
    await core_chat_bot.bot.send_message(chat_id=chat_id, text=text)
    return {"status": "success"}


@router.post("/{chat_id}/files")
async def chat_student_files(chat_id: str, text: str, files: list[UploadFile]):
    media_group = MediaGroupBuilder(caption=text)

    for file in files:
        doc = BufferedInputFile(file.file.read(), file.filename)
        media_group.add_photo(doc)

    build_media = media_group.build()

    await core_chat_bot.bot.send_media_group(chat_id=chat_id, media=build_media)

    return {"status": "success"}


@router.post("/{chat_id}/photos")
async def chat_student_files(chat_id: str, text: str, files: list[UploadFile]):
    media_group = MediaGroupBuilder(caption=text)

    for file in files:
        doc = BufferedInputFile(file.file.read(), file.filename)
        media_group.add_photo(doc)

    build_media = media_group.build()

    await core_chat_bot.bot.send_media_group(chat_id=chat_id, media=build_media)

    return {"status": "success"}
