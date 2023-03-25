import schedule
import time
from src.db_clients import db_client_runners
from src.sentry_logging.base_logging import *
from src.tg_bots import tg_poster
from src.runners.constants import USED_PARSERS, POST_EVERY_MINUTES
from src.sentry_logging.sentry_runners_logger import *

logger = logging.getLogger(__name__)


def do_post_in_telegram():
    try:
        logger.info(f'Function (do_post_in_telegram) is started')
        parser_names = list(map(lambda el: el.get_parser_name(), USED_PARSERS))
        posts = db_client_runners.get_all_not_posted_flats(parser_names)[:16]
        for post in posts:
            post_message = f'<b>{post[3]}</b>\n'
            post_message += f'<b>Цена: </b> {post[2]} BYN\n'
            post_message += f'<b>Описание: </b> {post[4][:100]}...\n'
            post_message += f'<i>см. источник {post[0]}</i>\n\n'
            post_message += '\n'.join(list(map(lambda el: el, post[6].split(',')[:6])))
            tg_poster.send_tg_post(post_message)
            time.sleep(1)
        db_client_runners.update_is_posted_state(list(map(lambda el: el[7], posts)))
    except(Exception,):
        logger.exception(f'Exception is occurred in (do_post_in_telegram)', {traceback.format_exc()})


schedule.every(POST_EVERY_MINUTES).minutes.do(do_post_in_telegram)

while True:
    schedule.run_pending()
    time.sleep(1)
