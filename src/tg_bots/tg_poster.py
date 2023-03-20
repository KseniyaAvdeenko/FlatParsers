from logging import getLogger

import telebot
from src.creds import TOKEN, REPORT_GROUP_ID
from sentry_logger_telegrambot import *

# https://t.me/flat_parserBot

logger = getLogger(__name__)
logger_func = logging_func(logger=logger)


bot = telebot.TeleBot(TOKEN)


@logger_func
def send_tg_post(message):
    bot.send_message(REPORT_GROUP_ID, message, parse_mode='html')

