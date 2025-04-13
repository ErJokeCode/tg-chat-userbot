from aiogram import Bot


class CoreBot():
    def __init__(self, token: str):
        self.__token = token
        self.bot = Bot(token=self.__token)
