from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types  import Message

import telegram_bot.keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Hi! \n'
                        f'Your name is {message.from_user.first_name}',
                        reply_markup=await kb.inline_cars())

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('This is the /help command')

@router.message(F.text == 'How is life?')
async def how_are_you(message: Message):
    await message.answer("Life's good")

@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'Photo ID: {message.photo[-1].file_id}')

@router.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAMVZ3bhJBxMix23W_qGsiTVqyrpD4QAAj_oMRuJL7hLGcsvGbE8C3QBAAMCAAN5AAM2BA',
                               caption='This is the awesome car!')

@router.message()
async def echo(message:Message):
    await message.answer(message.text)
