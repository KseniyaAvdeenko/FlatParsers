import threading
import schedule
import time
from constants import USED_PARSERS


def parse_all():
    for parser in USED_PARSERS:
        thread = threading.Thread(target=parser.update_with_last_flats)
        thread.start()


schedule.every(5).seconds.do(parse_all)

while True:
    schedule.run_pending()
    time.sleep(1)
