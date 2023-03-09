from src.creds import TG_TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import string
import random

# https://t.me/FindFlatsBot


bot = Bot(TG_TOKEN)
dp = Dispatcher(bot)

# def get_all_cities():


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Welcome',
                           reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp)
