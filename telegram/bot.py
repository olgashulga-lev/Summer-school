import asyncio
import configparser
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from handlers.init import register_handlers

config = configparser.ConfigParser()
config.read('config.ini')

bot = Bot(
    token=config['DEFAULT']['TOKEN'],
    default=DefaultBotProperties(parse_mode="HTML")
)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def set_commands():
    commands = [
        BotCommand(command="start", description="Главное меню"),
        BotCommand(command="registration", description="Создать персонажа"),
    ]
    await bot.set_my_commands(commands)


async def on_startup():
    await set_commands()
    print("Бот запущен!")


async def main():
    register_handlers(dp)

    await on_startup()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())