import logging
from src.creds import TG_TOKEN
from aiogram import Bot, Dispatcher, executor, types
from src.tg_bots.tg_bot_keyboards import *
from src.db_clients import db_client_tg_bot
from sentry_logger_telegrambot import *

# https://t.me/FindFlatsBot

logger = logging.getLogger(__name__)
logger_func = logging_func(logger=logger)

bot = Bot(TG_TOKEN)
dp = Dispatcher(bot)
user_query = {}

SUB_TEXT = """<b>‼ Хотите первыми узнавать самые лучшие предложения? </b>\n
<b>🔔Оформите подписку всего за 9.99 BYN ‼</b> \n
и первыми узнаете о квартирах по 📉️ самыми низкими ценами за кв.м. по району"""


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_query['user_id'] = str(message.from_user.id)
    user_query['username'] = message.from_user.username
    db_client_tg_bot.UserQuery().insert_userid_username(user_query)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро пожаловать в бот 👋🏻',
                           reply_markup=main_menu())


@dp.message_handler()
@logger_func
async def search_flats(message: types.Message):
    if message.text == '🔎 Искать квартиры в Минске 🔍':
        user_query['selected_city'] = 'г.Минск'
        db_client_tg_bot.UserQuery().insert_selected_city(user_query)
        await message.answer(text='Выберите район Минска', reply_markup=get_districts())
    all_districts = list(map(get_items_from_query, db_client_tg_bot.get_districts()))
    if message.text in all_districts:
        user_query['selected_district'] = message.text
        db_client_tg_bot.UserQuery().insert_selected_district(user_query)
        await message.answer(text="Выберите количество комнат",
                             reply_markup=get_rooms_by_district(message.text))
    all_rooms = [str(r) for r in range(1, 7)]
    if message.text in all_rooms:
        user_query['selected_rooms'] = int(message.text)
        db_client_tg_bot.UserQuery().insert_selected_rooms(user_query)
        await message.answer(text='Критерии просмотра', reply_markup=flats_show_criteria())

    if message.text == view_criteria[0]:
        user_query['selected_query'] = "SELECT link, title, price, square, micro_district, street, house_number," \
                                       " photo_links FROM flats WHERE city = %s and district = %s and" \
                                       " rooms_quantity = %s LIMIT 10;"
        db_client_tg_bot.UserQuery().insert_selected_query(user_query)
        await message.answer(
            text=generate_message_all_flats(str(message.from_user.id)),
            parse_mode='html',
            reply_markup=btn_back()
        )
    elif message.text == view_criteria[1]:
        user_query['selected_query'] = "SELECT link, title, price, square, micro_district, street, house_number," \
                                       " photo_links FROM flats WHERE city = %s and district = %s" \
                                       " and rooms_quantity = %s order by price asc LIMIT 10;"
        db_client_tg_bot.UserQuery().insert_selected_query(user_query)
        await message.answer(
            text=generate_message_all_flats(str(message.from_user.id)),
            parse_mode='html',
            reply_markup=btn_back()
        )
    elif message.text == view_criteria[2]:
        user_query['selected_query'] = "SELECT link, title, price, square, micro_district, street, house_number," \
                                       " photo_links FROM flats WHERE city = %s and district = %s and" \
                                       " rooms_quantity = %s order by price desc LIMIT 10;"
        db_client_tg_bot.UserQuery().insert_selected_query(user_query)
        await message.answer(
            text=generate_message_all_flats(str(message.from_user.id)),
            parse_mode='html',
            reply_markup=btn_back()
        )
    elif message.text == view_criteria[3]:
        user_query['selected_query'] = "SELECT link, title, price, square, micro_district, street, house_number," \
                                       " photo_links, update_date FROM flats WHERE city = %s and district = %s" \
                                       " and rooms_quantity = %s order by update_date desc LIMIT 10;"
        db_client_tg_bot.UserQuery().insert_selected_query(user_query)
        await message.answer(
            text=generate_message_all_flats(str(message.from_user.id)),
            parse_mode='html',
            reply_markup=btn_back())
    elif message.text == view_criteria[4]:
        user_query['selected_query'] = "SELECT link, title, price, square, micro_district, street, house_number," \
                                       " photo_links, update_date FROM flats WHERE city = %s and district = %s" \
                                       " and rooms_quantity = %s order by update_date asc LIMIT 10;"
        db_client_tg_bot.UserQuery().insert_selected_query(user_query)
        await message.answer(text=generate_message_all_flats(str(message.from_user.id)), parse_mode='html')
    elif message.text == view_criteria[5]:
        user_query['selected_query'] = "SELECT link, title, price, square, micro_district, street, house_number," \
                                       " photo_links, update_date FROM flats WHERE city = %s and district = %s" \
                                       " and rooms_quantity = %s order by square asc LIMIT 10;"
        db_client_tg_bot.UserQuery().insert_selected_query(user_query)
        await message.answer(
            text=generate_message_all_flats(str(message.from_user.id)),
            parse_mode='html',
            reply_markup=btn_back()
        )
    elif message.text == view_criteria[6]:
        user_query['selected_query'] = "SELECT link, title, price, square, micro_district, street, house_number," \
                                       " photo_links, update_date FROM flats WHERE city = %s and district = %s" \
                                       " and rooms_quantity = %s order by square desc LIMIT 10;"
        db_client_tg_bot.UserQuery().insert_selected_query(user_query)
        await message.answer(
            text=generate_message_all_flats(str(message.from_user.id)),
            parse_mode='html',
            reply_markup=btn_back()
        )

    if message.text == '🔙 Вернуться':
        await bot.send_message(chat_id=message.from_user.id,
                               text='Вы вернулись в главное меню',
                               reply_markup=main_menu())
    if message.text == '🔔 Оформить подписку 🔔':
        await message.answer(text=SUB_TEXT,
                             parse_mode='HTML',
                             reply_markup=subscribtion())


if __name__ == '__main__':
    executor.start_polling(dp)

