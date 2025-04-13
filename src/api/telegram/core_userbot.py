from telethon import TelegramClient  # type: ignore
from config import settings


class CoreUserBot:
    def __init__(
        self,
        session_name: str,
        api_id: int,
        api_hash: str,
        phone: str,
        password: str
    ):
        self.__api_id = api_id
        self.__api_hash = api_hash
        self.__phone = phone
        self.__session_name = session_name
        self.__password = password

        self.client = TelegramClient(
            self.__session_name,
            self.__api_id,
            self.__api_hash,
        )

    async def connect(self):
        await self.client.start(
            phone=self.__phone,
            password=self.__password
        )

    async def disconnect(self):
        await self.client.disconnect()


core_user_bot = CoreUserBot(
    settings.TG_SESSION_NAME,
    settings.TG_API_ID,
    settings.TG_API_HASH,
    settings.TG_PHONE,
    settings.TG_2FA_PASSWORD
)
