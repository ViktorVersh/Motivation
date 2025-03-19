import asyncio
import logging

from aiogram import Dispatcher, Bot

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

import config
# import config  # настройка конфигурации подключение Токена
from start import router  # подключение модуля commands
from dbase import db
from motiv import motiv_router

# настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)  # loop не нужен, aiogram сам управляет циклом событий


async def set_bot_commands():
    """
    Устанавливаем стартовое меню бота в виде
    кнопки на строке ввода сообщений
    """
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Запустить бота"),
        ]
    )


async def main():
    # Инициализация бота и диспетчера

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    dp.include_router(motiv_router)

    # Запуск бота
    await set_bot_commands()
    try:
        if not await db.create_tables():
            logging.info('Таблица уже существуют.')
        else:
            await db.create_tables()
            logging.info('Таблица созданы.')
        await dp.start_polling(bot)  # aiogram сам обрабатывает исключения
    except KeyboardInterrupt:
        await bot.close()  # важно корректно закрыть бот
        logging.info("Бот остановлен.")
    except Exception as e:
        logging.exception(f"Произошла ошибка: {e}")  # Логирование ошибок
        await bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())  # Упрощен запуск
    except KeyboardInterrupt:
        logging.info("Бот остановлен.")