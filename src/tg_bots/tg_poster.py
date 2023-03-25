from logging import getLogger
import telebot
from src.creds import TOKEN, REPORT_GROUP_ID
from src.sentry_logging.base_logging import logging_func
from src.sentry_logging.sentry_logger_telegrambot import *

# https://t.me/flat_parserBot

logger = logging.getLogger(__name__)
logger_func = logging_func(logger=logger)

bot = telebot.TeleBot(TOKEN)


@logger_func
def send_tg_post(message):
    bot.send_message(REPORT_GROUP_ID, message, parse_mode='html')

