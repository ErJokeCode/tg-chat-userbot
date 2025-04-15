import tempfile
from aiogram.types.input_file import BufferedInputFile
from aiogram.utils.media_group import MediaGroupBuilder

import os
import shutil
from fastapi import APIRouter, UploadFile

from api.telegram.core_bot import core_info_bot

router = APIRouter(
    prefix="/send",
    tags=["Send"],
)


@router.post("/files")
async def send_text_with_file(chat_ids: list[str], text: str, files: list[UploadFile]):
    media_group = MediaGroupBuilder(caption=text)

    for file in files:
        doc = BufferedInputFile(file.file.read(), file.filename)
        media_group.add_photo(doc)

    build_media = media_group.build()
    for id in chat_ids:
        await core_info_bot.bot.send_media_group(chat_id=id, media=build_media)

    return {"status": "success"}


@router.post("/photos")
async def send_text_with_photo(chat_ids: list[str], text: str, files: list[UploadFile]):
    media_group = MediaGroupBuilder(caption=text)

    for file in files:
        doc = BufferedInputFile(file.file.read(), file.filename)
        media_group.add_photo(doc)

    build_media = media_group.build()
    for id in chat_ids:
        await core_info_bot.bot.send_media_group(chat_id=id, media=build_media)

    return {"status": "success"}


@router.post("/{chat_id}")
async def send_text(chat_id: str, text: str):
    await core_info_bot.bot.send_message(chat_id=chat_id, text=text)
    return {"status": "success"}
