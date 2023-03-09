import schedule
import time
from src import db_client
from src.tg_bots import tg_poster
from src.runners.constants import USED_PARSERS


PARSE_EVERY_MINUTES = 2


def do_post_in_telegram():
    parser_names = list(map(lambda el: el.get_parser_name(), USED_PARSERS))
    posts = db_client.get_all_not_posted_flats(parser_names)[:16]
    for post in posts:
        post_message = f'<b>{post[3]}</b>\n'
        post_message += f'<b>Цена: </b> {post[2]} BYN\n'
        post_message += f'<b>Описание: </b> {post[4][:100]}...\n'
        post_message += f'<i>см. источник {post[0]}</i>\n\n'
        post_message += '\n'.join(list(map(lambda el: el, post[6].split(',')[:6])))
        tg_poster.send_tg_post(post_message)
        time.sleep(1)
    db_client.update_is_posted_state(list(map(lambda el: el[7], posts)))
    # print()

schedule.every(PARSE_EVERY_MINUTES).seconds.do(do_post_in_telegram)

while True:
    schedule.run_pending()
    time.sleep(1)
