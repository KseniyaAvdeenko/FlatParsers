# -*- coding: utf-8 -*-
import schedule
import time
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from src import db_client
from src.creds import HEADERS


def make_post_archived():
    flats = db_client.get_all_not_archived_flats()
    for flat in tqdm(flats, desc='Проверка квартир на архивный статус', colour='CYAN', ascii=False, dynamic_ncols=True,
                     unit=' квартир', position=0):
        response = requests.get(flat[0], headers=HEADERS)
        html = BeautifulSoup(response.content, 'html.parser')

        title = html.find('h1').text.strip()
        if title == flat[1]:
            continue
        else:
            db_client.update_is_archived_state(list(map(lambda el: el[2], flats)))
        print()


schedule.every(1).seconds.do(make_post_archived)
# schedule.every().day.at("00:00").do(make_post_archived)

while True:
    schedule.run_pending()
    time.sleep(1)