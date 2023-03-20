# -*- coding: utf-8 -*-
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from sentry_parsers_logger import *
import logging
from src.parsers.parser_interface import ParserInterface
from src.creds import HEADERS
from src.parsers.data import Flat


logger = logging.getLogger(__name__)
logger_func = logging_func(logger=logger)


class GoHomeParser(ParserInterface):

    def get_parser_name(self):
        return 'gohome'

    @logger_func
    def get_all_last_flats(self, page_from=0, page_to=1):
        flat_links = []
        while page_from < page_to:
            response = requests.get(f"https://gohome.by/sale/index/{page_from*30}", headers=HEADERS)
            html = BeautifulSoup(response.content, 'html.parser')
            links = html.find_all("a", {'href': True, 'class': 'name__link'})
            for a in links:
                flat_links.append(a['href'])
            page_from += 1
        ready_links = list(map(lambda el: 'https://gohome.by'+el, flat_links))
        return ready_links

    @logger_func
    def enrich_links_to_flats(self, links: list):
        flats = []
        for link in tqdm(links, desc='Парсинг квартир с gohome.by', colour='magenta', ascii=False, dynamic_ncols=True,
                         unit=' квартир', position=0):
            response = requests.get(link, headers=HEADERS)
            html = BeautifulSoup(response.content, 'html.parser')

            '''title'''
            try:
                title = html.find('h1').text.strip()
            except(Exception,):
                continue

            '''price'''
            try:
                price = int(re.sub('[^0-9]', '', html.find('div', class_='price big').span.text.replace(' ', '')))
            except(Exception,):
                price = 0

            '''description'''
            description = html.find('article').text.strip()

            '''seller_phone'''
            try:
                seller_phone = re.sub('[^0-9|(|)|+]', '', html.find('a', class_='phone__link').text.strip())
            except(Exception,):
                seller_phone = 'Не указано'

            '''rooms_quantity, square, house_year, date, city, district, micro_district'''
            try:
                li_list = html.find_all('li', class_='li-feature')
                name_list = []
                description_list = []
                for li in li_list[7:]:
                    for div_name in li.find_all('div', class_='name'):
                        name = div_name.text.strip()
                        name_list.append(name)
                    for div_description in li.find_all('div', class_='description'):
                        if div_description.find('a') in div_description:
                            a = div_description.find('a').text.strip()
                            description_list.append(a)
                        else:
                            desc = div_description.text.strip()
                            description_list.append(desc)
                info_common_dict = dict(zip(name_list, description_list))
                rooms_quantity = int(re.sub('[^0-9]', '', info_common_dict['Комнат:']))
                raw_square = re.split(r'[ ]', info_common_dict['Площадь общая:'])
                square = float(raw_square[0])
                house_year = int(re.sub('[^0-9]', '', info_common_dict['Год постройки:']))
                date = datetime.strptime(info_common_dict['Дата обновления:'], '%d.%m.%Y')
                city = 'г.' + info_common_dict['Населенный пункт:']

                district = info_common_dict['Район:']
                micro_district = info_common_dict['Микрорайон:']

                '''Address: street, house_number'''
                address = list(filter(lambda el: el != '', re.split(r'[,|.| ]', info_common_dict['Улица, дом:'])))
                street = address[0] + '. ' + address[1]
                house_number = ''
                if address[3] in address:
                    house_number = address[2] + '. ' + address[3]
            except(Exception,):
                continue

            '''price_for_meter'''
            try:
                price_for_meter = price // square
            except(Exception,):
                price_for_meter = 0

            '''images'''
            try:
                image_sections = html.find('div', class_="w-advertisement-images").find_all('img', class_="zlazy")
                images = list(map(lambda el: 'https://gohome.by' + el['data-zlazy'], image_sections))
            except(Exception,):
                images = []
            flats.append(Flat(
                link=link,
                reference=self.get_parser_name(),
                price=price,
                title=title,
                description=description,
                date=date,
                square=square,
                city=city,
                street=street,
                house_number=house_number,
                district=district,
                micro_district=micro_district,
                house_year=house_year,
                rooms_quantity=rooms_quantity,
                seller_phone=seller_phone,
                images=images,
                price_for_meter=price_for_meter
            ))
        return flats

# GoHomeParser().update_with_last_flats(0, 300)
