import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.types.web_app_info import WebAppInfo
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)

TOKEN = '7408980611:AAHiXQmEhmrvX8sEfWVEv2ZsUjZPJkGjBIw'
dp = Dispatcher()

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    btn = types.InlineKeyboardButton(text='Бот', url='https://t.me/footbetFunBot')
    button_row = [btn]
    markup = types.InlineKeyboardMarkup(inline_keyboard=[button_row])
    await message.answer('Привет!', reply_markup=markup)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
