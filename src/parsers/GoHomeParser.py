# -*- coding: utf-8 -*-
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from src.parsers.parser_interface import ParserInterface
from src.creds import HEADERS
from src.data import Flat


class GoHomeParser(ParserInterface):

    def get_parser_name(self):
        return 'gohome'

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

            '''price_for_meter'''
            try:
                price_for_meter = int(re.sub('[^0-9]', '', html.find('div', class_='price').text.replace(' ', '')))
            except(Exception,):
                price_for_meter = 0

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
                        feature = div_description.text.strip()
                        description_list.append(feature)
                info_common_dict = dict(zip(name_list, description_list))
                rooms_quantity = int(re.sub('[^0-9]', '', info_common_dict['Комнат:']))
                square = float(re.sub('[^0-9|.]', '', info_common_dict['Площадь общая:']))
                house_year = int(re.sub('[^0-9]', '', info_common_dict['Год постройки:']))
                date = datetime.strptime(info_common_dict['Дата обновления:'], '%d.%m.%Y')
                city = info_common_dict['Населенный пункт:']
                district = info_common_dict['Район:']
                micro_district = info_common_dict['Микрорайон:']

                '''Address: street, house_number'''
                address = re.split(r'[,|.]', info_common_dict['Улица, дом:'])

                street = address[0] + '. ' + address[2]
                house_number = 0
                if address[6] in address:
                    house_number = address[4] + '. ' + address[6]
            except(Exception,):
                date = datetime.now()
                rooms_quantity = 0
                square = 0
                house_year = 0
                city = 'Не указано'
                district = 'Не указано'
                micro_district = 'Не указано'
                street = 'Не указано'
                house_number = 'Не указано'

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


# GoHomeParser().update_with_last_flats(0, 334)
