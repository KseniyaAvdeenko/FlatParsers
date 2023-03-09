import telebot
from src.creds import TOKEN, REPORT_GROUP_ID

# https://t.me/flat_parserBot


bot = telebot.TeleBot(TOKEN)


def send_tg_post(message):
    bot.send_message(REPORT_GROUP_ID, message, parse_mode='html')
