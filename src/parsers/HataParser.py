# -*- coding: utf-8 -*-
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
from tqdm import tqdm
from src.creds import HEADERS
from src.data import Flat
from src.parsers.parser_interface import ParserInterface


class HataParser(ParserInterface):

    def get_parser_name(self):
        return 'hata'

    def get_all_last_flats(self, page_from=1, page_to=2):
        flat_links = []
        while page_from < page_to:
            response = requests.get(f"https://www.hata.by/sale-flat/page/{page_from}/", headers=HEADERS)
            html = BeautifulSoup(response.content, 'html.parser')
            links = html.find_all("a", href=True)
            for a in links:
                flat_links.append(a['href'])
            page_from += 1
        ready_links = list(filter(lambda el: 'object' in el, flat_links))
        return ready_links

    def enrich_links_to_flats(self, links):
        flats = []
        for link in tqdm(links, desc='Парсинг квартир с hata.by', colour='yellow', ascii=False, dynamic_ncols=True,
                         unit=' квартира', position=0):
            resp = requests.get(link, headers=HEADERS)
            html = BeautifulSoup(resp.content, 'html.parser')

            '''title'''
            title = html.find('h1', class_='b-card__title').text.strip()

            '''price with currency parser from https://myfin.by/bank/kursy_
            valjut_nbrb because price is calculated in $$ but not in BYN'''
            try:
                response = requests.get('https://myfin.by/bank/kursy_valjut_nbrb', headers=HEADERS)
                cur_html = BeautifulSoup(response.content, 'html.parser')
                actual_currency = float(cur_html.find('tr', {'data-key': 0}).find_all('td')[1].text)
                price = int(re.sub('[^0-9]', '', html.find('div', class_='value').text.strip())) * actual_currency
            except(Exception,):
                price = 0

            '''description'''
            description = html.find('div', class_='description').text.strip()

            '''rooms_quantity & square'''
            try:
                square_rooms_info_keys = []
                square_rooms_info_values = []
                for info in html.find_all('tbody')[0].find_all('td', class_=False):
                    info_keys = info.text
                    square_rooms_info_keys.append(info_keys)
                for info in html.find_all('tbody')[0].find_all('td', class_='value'):
                    info_values = re.sub('[\n|' ']', '', info.text.strip())
                    square_rooms_info_values.append(info_values)
                square_rooms_info_dict = dict(zip(square_rooms_info_keys, square_rooms_info_values))
                rooms_quantity = int(square_rooms_info_dict['Комнат'])
                square = float(re.sub('[^0-9|.]', '', square_rooms_info_dict['Общая площадь']))
            except (Exception,):
                rooms_quantity = 'Не указан'
                square = 'Не указан'

            '''house_year'''
            try:
                house_year_info_keys_list = []
                house_year_info_values_list = []
                for info in html.find_all('tbody')[1].find_all('td', class_=False):
                    info_keys = re.sub('[\n|' ']', '', info.text.strip())
                    house_year_info_keys_list.append(info_keys)
                for info in html.find_all('tbody')[1].find_all('td', class_='value'):
                    info_values = re.sub('[\n|' ']', '', info.text.strip())
                    house_year_info_values_list.append(info_values)
                table_house_dict = dict(zip(house_year_info_keys_list, house_year_info_values_list))
                house_year = table_house_dict['Год постройки']
            except (Exception,):
                house_year = 'Не указан'

            '''date'''
            try:
                date_info_keys_list = []
                date_info_values_list = []
                for info in html.find_all('tbody')[2].find_all('td', class_=False):
                    info_keys = re.sub('[\n|' ']', '', info.text.strip())
                    date_info_keys_list.append(info_keys)
                for info in html.find_all('tbody')[2].find_all('td', class_='value'):
                    info_values = re.sub('[\n|' ']', '', info.text.strip())
                    date_info_values_list.append(info_values)
                table_date_dict = dict(zip(date_info_keys_list, date_info_values_list))
                date = datetime.strptime(table_date_dict['Дата обновления'], '%d.%m.%Y')
            except (Exception,):
                date = datetime.now()

            '''address: city, street, house_number'''
            try:
                address = re.split(r'[|,|\b|\s]',
                                   html.find('div',
                                             class_='b-card__address b-card__address_bottom').find('span').text.strip())
                city = address[1]
                street = address[4] + ' ' + address[5]
                house_number = address[7]
            except (Exception,):
                city = 'Не указан'
                street = 'Не указан'
                house_number = 'Не указан'

            '''district & micro_district'''
            try:
                district = ''
                micro_district = ''
                for info in html.find_all('table', class_='i-table')[3].find('a'):
                    district = info.text.strip()
                for info in html.find_all('table', class_='i-table')[4].find_all('td'):
                    micro_district = info.text.strip()
            except (Exception,):
                district = 'Не указан'
                micro_district = 'Не указан'

            '''seller_phone'''
            try:
                seller_phone = html.find('div', class_='p_nm', string='Телефон').find_next().text.strip()
            except(Exception,):
                seller_phone = 'Не указан'

            '''images'''
            try:
                images = []
                image_links = list(filter(lambda el2: el2[:19] == 'https://pic.hata.by',
                                          (map(lambda el2: el2['src'], html.find_all("img")))))
                for img_links in image_links:
                    img_link = re.split(r'[&]+', img_links)[1][6:]
                    images.append(img_link)

            except(Exception,):
                images = []

            '''price_for_meter'''
            try:
                price_for_meter = price//square
            except(Exception,):
                price_for_meter = 0


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


# HataParser().enrich_links_to_flats(HataParser().get_all_last_flats())
# HataParser().update_with_last_flats(1, 10)
