from aiogram import Bot

from config import settings


class CoreBot():
    def __init__(self, token: str):
        self.__token = token
        self.bot = Bot(token=self.__token)


core_chat_bot = CoreBot(settings.TG_TOKEN_CHAT_BOT)
core_info_bot = CoreBot(settings.TG_TOKEN_INFO_BOT)
