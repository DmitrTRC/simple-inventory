import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.handlers import router
from dotenv import load_dotenv
from utils.logging_simp_inv import setup_logging

load_dotenv()
bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(storage=MemoryStorage())


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    setup_logging()
    asyncio.run(main())
