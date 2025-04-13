import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

import asyncio

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # noqa

from config import settings
from handlers import start, main_menu, information_teaching, faq, onboarding
from info_bot.worker import Worker, manager_onboarding, manager_faq

_log = logging.getLogger(__name__)

storage = RedisStorage.from_url(settings.URL_REDIS)

bot = Bot(token=settings.TG_TOKEN_INFO_BOT)
dp = Dispatcher(storage=storage)
dp.include_routers(start.router, main_menu.router,
                   information_teaching.router, faq.router, onboarding.router)


async def main():
    _log.info("Bot started")

    worker = Worker(10, settings.AUTH_CORE_SERVER)
    worker.add_manager_onboarding(
        manager_onboarding, settings.URL_CORE_SERVER + "/parser/bot/onboard/")
    worker.add_manager_faq(
        manager_faq, settings.URL_CORE_SERVER + "/parser/bot/faq/")
    asyncio.create_task(worker.work())

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
