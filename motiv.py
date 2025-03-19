import logging
import os
import sys

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

import keyboard
from dbase import db

motiv_router = Router()  # Создание роутера
storage = MemoryStorage()  # Создание кэша памяти


async def menu_motiv(message: types.Message):
    await message.answer(' *Выберите нужный Вам раздел с помощью меню* 😎', reply_markup=keyboard.stinfo)


# Функция получения мотивации на день
@motiv_router.message(F.text == "✅Мотивация для Вас")
async def get_motivation(message: types.Message, state: FSMContext):
    try:
        # Проверяем, есть ли записи в базе данных
        has_records = await db.has_records_in_table('Motivation')
        print("Проверка наличия записей:", has_records)

        if not has_records:
            await message.answer("Подождите...🕐")

            # Проверим сначала наличие файла
            if os.path.exists('motivation.txt'):
                with open('motivation.txt', 'r', encoding='utf-8') as file:
                    for line in file:
                        motiv_text = line.strip()
                        print(motiv_text)
                        await db.add_motiv(motiv_text)
                await message.answer("Ок!🏁")

            else:
                await message.answer("Файл с мотивациями не найден. Мотивации не добавлены.")
                return

        # Получаем случайную мотивацию
        motiv = await db.get_random_motivation()
        print("Мотивация:", motiv)
        if motiv:
            await message.answer(f"✅ {motiv}")
        else:
            await message.answer("😒 Не удалось получить мотивацию. Попробуйте позже.")

    except Exception as e:
        logging.error(f"Ошибка при получении мотивации: {e}, строка {sys.exc_info()[2].tb_lineno}")
        await message.answer("Произошла ошибка при получении мотивации. Пожалуйста, попробуйте позже.")


# Информация о боте
@motiv_router.message(F.text == "📖Информация о боте")
async def about_motiv(message: types.Message):
    await message.answer("🟩Бот мотивации создан для людей, которые стремятся к успеху и достижению своих целей.\n "
                         "🟩Бот предоставляет мотивирующие сообщения, которые помогают пользователям "
                         "поддерживать позитивный настрой и двигаться вперед. \n"
                         "🟩Бот также предлагает пользователю оставить свой текст мотивации "
                         "и мотивировать других пользователей.")