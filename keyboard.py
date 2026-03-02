from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

stinfo = ReplyKeyboardMarkup(resize_keyboard=True,
                             input_field_placeholder="🟢Воспользуйтесь меню:",
                             keyboard=[
                                 [KeyboardButton(text='✅Мотивация для Вас'),
                                  KeyboardButton(text='🖊Дополнить базу')],
                                 [KeyboardButton(text='📖Информация о боте'),]
                             ]
                             )
