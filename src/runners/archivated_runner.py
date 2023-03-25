# -*- coding: utf-8 -*-
import traceback
import schedule
import time
import requests
from src.db_clients import db_client_runners
from src.creds import HEADERS
from src.runners.constants import ARCHIVE
from src.sentry_logging.base_logging import *
from src.sentry_logging.sentry_runners_logger import *

logger = logging.getLogger(__name__)


def make_post_archived():
    try:
        logger.info(f'Function (make_post_archived) is started')
        flats = db_client_runners.get_all_not_archived_flats()
        flats_with_response = list(map(lambda el: (el[0], requests.get(el[1], headers=HEADERS)), flats))
        flats_to_archive = list(
            filter(lambda el: el[1].status_code == 404 or (len(el[1].history) and el[1].history[0].status_code == 301),
                   flats_with_response))
        db_client_runners.update_is_archived_state(list(map(lambda el: el[0], flats_to_archive)))
    except(Exception,):
        logger.exception(f'Exception is occurred in ((make_post_archived))', {traceback.format_exc()})


schedule.every().day.at(ARCHIVE).do(make_post_archived)

while True:
    schedule.run_pending()
    time.sleep(1)
