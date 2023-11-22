from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           InlineQueryResultArticle, InputTextMessageContent,
                           KeyboardButton, ReplyKeyboardMarkup)

kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Генерация картинки'), KeyboardButton(text='Chat GPT')], [KeyboardButton(text='Погода')]], resize_keyboard=True)

kb_weather = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Поделиться местоположением',
                    request_location=True, resize_keyboard=True)]
])

ikb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(
        text='inst', url='https://instagram.com/boziesvet?igshid=OGQ5ZDc2ODk2ZA=='),
    InlineKeyboardButton(text='Vk', url='https://vk.com/b0z1esv3t')]], resize_keyboard=True)