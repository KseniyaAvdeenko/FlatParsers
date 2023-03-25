# -*- coding: utf-8 -*-
import threading
import schedule
import time
from constants import USED_PARSERS, PARSE_EVERY_MINUTES
from src.sentry_logging.base_logging import *
from src.sentry_logging.sentry_runners_logger import *

logger = logging.getLogger(__name__)


def parse_all():
    try:
        logger.info(f'Function (parse_all) is started')
        for parser in USED_PARSERS:
            thread = threading.Thread(target=parser.update_with_last_flats, args=(0, 50))
            thread.start()
            thread.join()
    except(Exception,):
        logger.exception(f'Exception is occurred in (parse_all)', {traceback.format_exc()})


schedule.every(PARSE_EVERY_MINUTES).minutes.do(parse_all)

while True:
    schedule.run_pending()
    time.sleep(1)
