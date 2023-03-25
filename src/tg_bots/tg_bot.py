from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from src.creds import TG_TOKEN, PAYMENTS_TOKEN
from aiogram import Bot, Dispatcher, executor, types

from src.sentry_logging.base_logging import logging_func
from src.tg_bots.tg_bot_keyboards import *
from src.db_clients import db_client_tg_bot
from src.sentry_logging.sentry_logger_telegrambot import *

# https://t.me/FindFlatsBot

logger = logging.getLogger(__name__)

bot = Bot(TG_TOKEN)
dp = Dispatcher(bot)
user_query = {}

PRICE = types.LabeledPrice(label="Подписка на 1 месяц", amount=10 * 100)  # в копейках (руб)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_query['user_id'] = str(message.from_user.id)
    user_query['username'] = message.from_user.username
    db_client_tg_bot.UserQuery().insert_userid_username(user_query)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро пожаловать в бот 👋🏻',
                           reply_markup=main_menu())


@dp.message_handler()
async def search_flats(message: types.Message):
    try:
        logger.info(f'Function (search_flats) is started')
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
                                           " rooms_quantity = %s LIMIT 15;"
            db_client_tg_bot.UserQuery().insert_selected_query(user_query)
            await message.reply(
                show_results(message, str(message.from_user.id)),
                parse_mode='html', reply_markup=btn_back()
            )
        elif message.text == view_criteria[1]:
            user_query['selected_query'] = "SELECT link, title, price, square, micro_district, street, house_number," \
                                           " photo_links FROM flats WHERE city = %s and district = %s" \
                                           " and rooms_quantity = %s order by price asc LIMIT 15;"
            db_client_tg_bot.UserQuery().insert_selected_query(user_query)
            await message.reply(show_results(
                message, str(message.from_user.id)),
                parse_mode='html',
                reply_markup=btn_back()
            )
        elif message.text == view_criteria[2]:
            user_query['selected_query'] = "SELECT link, title, price, square, micro_district, street, house_number," \
                                           " photo_links FROM flats WHERE city = %s and district = %s and" \
                                           " rooms_quantity = %s order by price desc LIMIT 15;"
            db_client_tg_bot.UserQuery().insert_selected_query(user_query)
            await message.reply(show_results(message, str(message.from_user.id)),
                                parse_mode='html', reply_markup=btn_back()
                                )
        elif message.text == view_criteria[3]:
            user_query['selected_query'] = "SELECT link, title, price, square, micro_district, street, house_number," \
                                           " photo_links, update_date FROM flats WHERE city = %s and district = %s" \
                                           " and rooms_quantity = %s order by update_date desc LIMIT 15;"
            db_client_tg_bot.UserQuery().insert_selected_query(user_query)
            await message.reply(show_results(message, str(message.from_user.id)), parse_mode='html',
                                reply_markup=btn_back())
        elif message.text == view_criteria[4]:
            user_query['selected_query'] = "SELECT link, title, price, square, micro_district, street, house_number," \
                                           " photo_links, update_date FROM flats WHERE city = %s and district = %s" \
                                           " and rooms_quantity = %s order by update_date asc LIMIT 15;"
            db_client_tg_bot.UserQuery().insert_selected_query(user_query)
            await message.reply(show_results(message, str(message.from_user.id)), parse_mode='html',
                                reply_markup=btn_back())
        elif message.text == view_criteria[5]:
            user_query['selected_query'] = "SELECT link, title, price, square, micro_district, street, house_number," \
                                           " photo_links, update_date FROM flats WHERE city = %s and district = %s" \
                                           " and rooms_quantity = %s order by square asc LIMIT 15;"
            db_client_tg_bot.UserQuery().insert_selected_query(user_query)
            await message.reply(show_results(message, str(message.from_user.id)), parse_mode='html',
                                reply_markup=btn_back())
        elif message.text == view_criteria[6]:
            user_query['selected_query'] = "SELECT link, title, price, square, micro_district, street, house_number," \
                                           " photo_links, update_date FROM flats WHERE city = %s and district = %s" \
                                           " and rooms_quantity = %s order by square desc LIMIT 15;"
            db_client_tg_bot.UserQuery().insert_selected_query(user_query)
            await message.reply(show_results(message, str(message.from_user.id)), parse_mode='html',
                                reply_markup=btn_back())

        if message.text == '🔙 Вернуться':
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Вы вернулись в главное меню',
                                   reply_markup=main_menu())

        if message.text == '🔔 Оформить подписку 🔔':
            await message.answer(text=SUB_TEXT,
                                 parse_mode='HTML',
                                 reply_markup=subscribtion())
        if message.text == '💰  Оформить подписку':
            if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
                await bot.send_message(message.chat.id, "Тестовый платеж!!!")
            await bot.send_invoice(message.chat.id,
                                   title="Подписка на бота",
                                   description="Активация подписки на 1 месяц",
                                   provider_token=PAYMENTS_TOKEN,
                                   currency="rub",
                                   photo_url='https://s0.rbk.ru/v6_top_pics/media/img/1/62/756371557475621.jpg',
                                   photo_width=416,
                                   photo_height=234,
                                   photo_size=416,
                                   is_flexible=False,
                                   prices=[PRICE],
                                   start_parameter="one-month-subscription",
                                   payload="test-invoice-payload")
    except(Exception,):
        logger.exception(f'Exception is occurred in (search_flats)', {traceback.format_exc()})


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")
    if message.text == f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!":
        user_query['selected_query'] = "SELECT link, title, price, square, micro_district, street, house_number," \
                                       " price_for_meter FROM flats WHERE price_for_meter < (SELECT AVG(price_for_meter))" \
                                       "AND city = %s AND district = %s AND rooms_quantity = %s " \
                                       "GROUP by link, title, price, square, micro_district, street, house_number," \
                                       " price_for_meter LIMIT 15;"
        db_client_tg_bot.UserQuery().insert_selected_query(user_query)
        await message.reply(show_results(message, str(message.from_user.id)), parse_mode='html',
                            reply_markup=btn_back())


if __name__ == '__main__':
    executor.start_polling(dp)
