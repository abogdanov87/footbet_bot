import asyncio
import logging
import requests
import sys
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.types.web_app_info import WebAppInfo
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)

URL = 'https://footbet.fun/api/v2/tournament-table/1/'
# URL = 'http://127.0.0.1:8000/api/v2/tournament-table/1/'
TOKEN = '7408980611:AAHiXQmEhmrvX8sEfWVEv2ZsUjZPJkGjBIw' # PROD
# TOKEN = '7163748824:AAHRLrUUW308fuQ5JzL39Z7K-SvfqEi_PQk' # TEST
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router(name=__name__)
dp.include_routers(router)


def get_table():
    info_msg = ""
    
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        info_msg = f"""<b>Турнирная таблица {data['title']}</b>

"""
        position = 1
        # participants = data['tournament_participant']
        participants = sorted(
            data['tournament_participant'], 
            key=lambda p: (
                p['score']['points'],
                p['score']['exact_result'],
                p['score']['goals_difference'],
                p['score']['match_result'],
                (p['user']['nickname'] or p['user']['username'])
            ), 
            reverse=True)
        # import pdb; pdb.set_trace()
        for participant in participants:
            username = participant['user']['nickname'] or participant['user']['username']
            score = participant['score']['points']
            if score - (score // 1) == 0:
                score = int(score)
            else:
                pass
            info_msg += f""" {username} — {score}
"""
            position = position + 1
    return info_msg


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    btn1 = types.InlineKeyboardButton(text='Бот', url='https://t.me/footbetFunBot')
    btn2 = types.InlineKeyboardButton(text='Таблица', callback_data='table')
    button_row = [btn1, btn2]
    markup = types.InlineKeyboardMarkup(inline_keyboard=[button_row])
    try:
        await message.delete()
    except:
        pass
    await message.answer('Привет!', reply_markup=markup)


@router.callback_query(F.data == 'table')
async def callback_query_handler(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    try:
        await callback_query.message.delete()
    except:
        pass
    await callback_query.bot.send_message(chat_id, get_table())


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
