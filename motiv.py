import logging
import os
import sys

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

import keyboard
from dbase import db
from Stat import Motiv

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

        if not has_records:
            await message.answer("Подождите...🕐")

            # Проверим сначала наличие файла
            if os.path.exists('motivation.txt'):
                with open('motivation.txt', 'r', encoding='utf-8') as file:
                    for line in file:
                        motiv_text = line.strip()
                        await db.add_motiv(motiv_text)
                await message.answer("Ок!🏁")

            else:
                await message.answer("Файл с мотивациями не найден. Мотивации не добавлены.")
                return

        # Получаем случайную мотивацию
        motiv = await db.get_random_motivation()
        # logging.info(motiv) # Для отладки
        if motiv:
            await message.answer(f"✅ {motiv}")
        else:
            await message.answer("😒 Не удалось получить мотивацию. Попробуйте позже.")

    except Exception as e:
        logging.error(f"Ошибка при получении мотивации: {e}, строка {sys.exc_info()[2].tb_lineno}")
        await message.answer("Произошла ошибка при получении мотивации. Пожалуйста, попробуйте позже.")


# Дополнение базы мотивацией
@motiv_router.message(F.text == "📝Дополнить базу")
async def motivation_create(message: types.Message, state: FSMContext):
    await message.answer("Напишите текст Вашей мотивации!")
    await state.set_state(Motiv.new_motiv)


# Обработка текста мотивации
@motiv_router.message(F.text == "📝Дополнить базу")
async def motivation_create(message: types.Message, state: FSMContext):
    await message.answer("Напишите текст Вашей мотивации!")
    await state.set_state(Motiv.new_motiv)  # Устанавливаем состояние


# Обработка текста мотивации
@motiv_router.message(Motiv.new_motiv)
async def process_motivation(message: types.Message, state: FSMContext):
    motiv_text = message.text  # Получаем текст мотивации

    # Проверка на пустой текст
    if not motiv_text or not motiv_text.strip():
        await message.answer("Текст мотивации не может быть пустым. Пожалуйста, введите текст.")
        return

    # Сохраняем текст мотивации в состоянии
    await state.update_data(motivation=motiv_text)

    # Получаем текст мотивации из состояния
    data = await state.get_data()
    motiv_text = data.get('motivation')  # Используем тот же ключ, что и при сохранении

    if not motiv_text:
        await message.answer("Текст мотивации не найден. Пожалуйста, попробуйте еще раз.")
        return

    try:
        # Сохраняем мотивацию в базу данных
        await db.add_motiv(f'"{motiv_text}" - {message.from_user.full_name}')
        await message.answer(f"Текст Вашей мотивации сохранён, "
                             f"{message.from_user.full_name}! "
                             f"Теперь он будет появляться в мотивации на каждый день.")
    except Exception as e:
        logging.error(f"Ошибка при сохранении текста мотивации: {e}")
        await message.answer("Произошла ошибка при сохранении текста мотивации. Пожалуйста, попробуйте позже.")
    finally:
        await state.clear()  # Очищаем состояние


# Информация о боте
@motiv_router.message(F.text == "📖Информация о боте")
async def about_motiv(message: types.Message):
    await message.answer("🟩Бот мотивации создан для людей, которые стремятся к успеху и достижению своих целей.\n "
                         "🟩Бот предоставляет мотивирующие сообщения, которые помогают пользователям "
                         "поддерживать позитивный настрой и двигаться вперед. \n"
                         "🟩Бот также предлагает пользователю оставить свой текст мотивации "
                         "и мотивировать других пользователей.")