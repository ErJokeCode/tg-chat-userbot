import asyncio
import uvicorn

from chat_bot import main as main_chat_bot


def start_api():
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)


def start_chat_bot():
    asyncio.run(main_chat_bot.main())


if __name__ == "__main__":
    asyncio.create_task(start_api())

    asyncio.create_task(start_chat_bot())
