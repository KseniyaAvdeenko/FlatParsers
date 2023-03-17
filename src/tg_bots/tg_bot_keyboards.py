from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton

from src.db_clients import db_client_tg_bot


def get_items_from_query(list_of_tuples: list[tuple]):
    for tuple_of_items in list_of_tuples:
        return tuple_of_items


def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    search_minsk_flats = KeyboardButton(text='🔎 Искать квартиры в Минске 🔍')
    subscription = KeyboardButton(text='🔔 Оформить подписку 🔔')
    kb.add(search_minsk_flats).add(subscription)
    return kb


def get_districts():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    all_districts = list(map(get_items_from_query, db_client_tg_bot.get_districts()))
    btn0 = KeyboardButton(text=all_districts[0])
    btn1 = KeyboardButton(text=all_districts[1])
    btn2 = KeyboardButton(text=all_districts[2])
    btn3 = KeyboardButton(text=all_districts[3])
    btn4 = KeyboardButton(text=all_districts[4])
    btn5 = KeyboardButton(text=all_districts[5])
    btn6 = KeyboardButton(text=all_districts[6])
    btn7 = KeyboardButton(text=all_districts[7])
    btn8 = KeyboardButton(text=all_districts[8])
    keyboard.add(btn0, btn1, btn2).add(btn3, btn4, btn5).add(btn6, btn7, btn8)
    btn_back = KeyboardButton(text='🔙 Вернуться')
    keyboard.add(btn_back)
    return keyboard


get_districts()


def get_rooms_by_district(district):
    room_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    rooms = list(sorted(filter(lambda el: el in range(1, 7),
                               map(get_items_from_query, db_client_tg_bot.get_rooms_by_district(district)))))
    all_rooms = list(map(str, rooms))
    for room in all_rooms:
        btn = KeyboardButton(text=room)
        room_keyboard.add(btn)
    btn_back = KeyboardButton(text='🔙 Вернуться')
    room_keyboard.add(btn_back)
    return room_keyboard


view_criteria = [
    'Показать все квартиры 📋',
    'Показать квартиры по цене(сначала дешевые)⬇️',
    'Показать квартиры по цене(сначала дорогие)⬆️',
    'Показать квартиры по дате(сначала новые)⬆️',
    'Показать квартиры по дате(сначала старые)⬇️',
    'Показать квартиры по площади(сначала маленькие)⬇️',
    'Показать квартиры по площади(сначала большие)⬆️'
]


def flats_show_criteria():
    criteria_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(text=view_criteria[0])
    btn2 = KeyboardButton(text=view_criteria[1])
    btn3 = KeyboardButton(text=view_criteria[2])
    btn4 = KeyboardButton(text=view_criteria[3])
    btn5 = KeyboardButton(text=view_criteria[4])
    btn6 = KeyboardButton(text=view_criteria[5])
    btn7 = KeyboardButton(text=view_criteria[6])
    criteria_keyboard.add(btn1).add(btn2, btn3, btn4).add(btn5, btn6, btn7)
    btn_back = KeyboardButton(text='🔙 Вернуться')
    criteria_keyboard.add(btn_back)
    return criteria_keyboard


def generate_message_all_flats(user_id):
    user_query_data = db_client_tg_bot.UserQuery().show_user_query(user_id)
    sql = user_query_data[0][6]
    data = (user_query_data[0][3], user_query_data[0][4], user_query_data[0][5])
    all_flats = db_client_tg_bot.show_flats_criteria(sql, data)
    message = f'''Найдено {len(all_flats)} квартиры\n\n'''
    for flat in all_flats:
        message += f"""🏠 <b>{flat[1]}</b>\n
        <b>Цена:</b> {flat[2]} BYN\n
        <b>Адрес:</b> {flat[5]}, д. {flat[6]}\n
        <b>Общая площадь:</b> {flat[3]} кв.м.\n
        <b>Источник:</b> {flat[0]}\n\n"""
    return message


def subscribtion():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text='💰  Оформить подписку', url=None)
    # more = KeyboardButton(text="Подробнее", url=None)
    back = KeyboardButton(text='🔙 Вернуться', callback_data='🔙 Вернуться')
    keyboard.add(back, btn)
    return keyboard


def btn_back():
    keyboard_back = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_back = KeyboardButton(text='🔙 Вернуться')
    keyboard_back.add(btn_back)
    return keyboard_back

