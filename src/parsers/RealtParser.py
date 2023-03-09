# -*- coding: utf-8 -*-
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from tqdm import tqdm
from src.parsers.parser_interface import ParserInterface
from src.creds import HEADERS
from src.data import Flat


class RealtParser(ParserInterface):

    def get_parser_name(self):
        return 'realt'

    def get_all_last_flats(self, page_from=1, page_to=2):
        flat_links = []

        while page_from < page_to:
            response = requests.get(f"https://realt.by/sale/flats/?page={page_from}", headers=HEADERS)
            html = BeautifulSoup(response.content, 'html.parser')
            links = html.find_all("a", href=True, class_='teaser-title')
            for a in links:
                flat_links.append(a['href'])
            page_from += 1
        ready_links = list(filter(lambda el: 'object' in el, flat_links))
        return ready_links

    def enrich_links_to_flats(self, links):
        flats = []
        for link in tqdm(links, desc='Парсинг квартир с realt.by', colour='yellow', ascii=False, dynamic_ncols=True,
                         unit=' квартир', position=0):
            response = requests.get(link, headers=HEADERS)
            html = BeautifulSoup(response.content, 'html.parser')
            # html.original_encoding
            '''title'''
            title = html.find('h1', class_='order-1').text.strip()

            '''price & price_for_meter'''
            try:
                price = int(re.sub('[^0-9]', '', html.find('h2', class_='w-full').text.strip()))
                price_for_meter = int(re.sub(
                    '[^0-9]', '', html.find(
                        'span', class_='mr-1.5 text-subhead sm:text-body text-basic').text.strip()))
            except(Exception,):
                price = 0
                price_for_meter = 0

            '''description'''
            description = html.find(
                'section',
                class_='bg-white flex flex-wrap md:p-6 my-4 rounded-md').find(
                'div', class_='w-full').text.strip()

            '''Common info: house_year, square, rooms_quantity'''
            try:
                common_info_list = []
                common_info_values_list = []
                for info in html.find('ul', class_='w-full -my-1').find_all('span'):
                    info_keys = info.text
                    common_info_list.append(info_keys)
                for info in html.find('ul', class_='w-full -my-1').find_all('p'):
                    info_values = info.text
                    common_info_values_list.append(info_values)
                info_dict = dict(zip(common_info_list, common_info_values_list))
                square = float(re.sub('[^0-9|.]', '', info_dict['Площадь общая']))
                rooms_quantity = int(info_dict['Количество комнат'])
                house_year = int(info_dict['Год постройки'])
            except (Exception,):
                rooms_quantity = 0
                square = 0
                house_year = 0

            '''location: city, street, house_number, district, micro_district'''
            try:
                house_num = {}
                location_info_list = []
                location_info_values_list = []
                for info in html.find('ul', class_='w-full mb-0.5 -my-1').find_all('span'):
                    if info.text == 'Номер дома':
                        house_num = {info.text: ''}
                    else:
                        loc_info_keys = info.text
                        location_info_list.append(loc_info_keys)
                for info in html.find('ul', class_='w-full mb-0.5 -my-1').find_all('a'):
                    info_values = re.sub("[\n|\xa0]", "", info.text.strip())
                    location_info_values_list.append(info_values)
                for p in html.find('ul', class_='w-full mb-0.5 -my-1').find_all('p'):
                    house_num['Номер дома'] = p.text

                info_location_dict = dict(zip(location_info_list, location_info_values_list))
                city = info_location_dict['Населенный пункт']
                street = info_location_dict['Улица']
                district = info_location_dict['Район города']
                micro_district = info_location_dict['Микрорайон']
                house_number = house_num['Номер дома']
            except (Exception,):
                city = 'Не указано'
                street = 'Не указано'
                micro_district = 'Не указано'
                house_number = 'Не указано'
                district = 'Не указано'

            '''date'''
            try:
                date = datetime.strptime(html.find('span', class_='mr-1.5').text.strip(), '%d.%m.%Y')
            except (Exception,):
                date = datetime.now()

            '''images'''
            try:
                images = set()
                image_divs = html.find_all('div', class_='swiper-slide')
                for image_div in image_divs:
                    for img in list(filter(lambda el: el is not None and (el[:4] =='http' and 'user' in el), map(lambda el2: el2['src'], image_div.find_all('img')))):
                        images.add(img)
                images = list(images)
            except(Exception,):
                images = []
            # seller_phone
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
                images=images,
                price_for_meter=price_for_meter
            ))
        return flats


# RealtParser().update_with_last_flats(1, 5)
