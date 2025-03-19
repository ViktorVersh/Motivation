from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from motiv import menu_motiv

router = Router()  # Создание роутера
storage = MemoryStorage()  # Создание хранилища


#  Стартовое приветствие

@router.message(Command("start"))  # Создание команды
async def send_welcome(message: types.Message):
    await message.answer(
        f'Добро пожаловать, {message.from_user.full_name}, в наш бот "мотивация на каждый день"! 😎\n '
    )
    await menu_motiv(message)
