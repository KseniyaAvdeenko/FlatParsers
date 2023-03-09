# -*- coding: utf-8 -*-
import threading
import schedule
import time
from constants import USED_PARSERS

PARSE_EVERY_MINUTES = 10


def parse_all():
    for parser in USED_PARSERS:
        thread = threading.Thread(target=parser.update_with_last_flats, args=(1, 200))
        thread.start()
        thread.join()


schedule.every(PARSE_EVERY_MINUTES).minutes.do(parse_all)

while True:
    schedule.run_pending()
    time.sleep(1)
