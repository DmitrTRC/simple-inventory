from aiogram.types import (KeyboardButton,
                           ReplyKeyboardMarkup,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Catalogue')],
    [KeyboardButton(text='Bin'), KeyboardButton(text='Contacts')]
],
    resize_keyboard=True,
    input_field_placeholder='Choose an option in the menu...'
)

settings= InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='YouTube', url='https://youtube.com')]
])


cars = ['Tesla', 'Mercedes', 'BMW']

async def inline_cars():
    keyboard = InlineKeyboardBuilder()
    for car in cars:
        keyboard.add(InlineKeyboardButton(text=car, url='https://youtube.com'))
    return keyboard.adjust(2).as_markup() # number of buttons per line