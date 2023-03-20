# -*- coding: utf-8 -*-
import threading
from logging import getLogger

import schedule
import time
from constants import USED_PARSERS
from sentry_runners_logger import *

PARSE_EVERY_MINUTES = 5


logger = getLogger(__name__)
logger_func = logging_func(logger=logger)


@logger_func
def parse_all():
    for parser in USED_PARSERS:
        thread = threading.Thread(target=parser.update_with_last_flats, args=(151, 300))
        thread.start()
        thread.join()


schedule.every(PARSE_EVERY_MINUTES).minutes.do(parse_all)

while True:
    schedule.run_pending()
    time.sleep(1)
