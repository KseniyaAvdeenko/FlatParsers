import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
from src.creds import HEADERS
from src.data import Flat
from src.parsers.parser_interface import ParserInterface
import PySimpleGUI as sg


class HataParser(ParserInterface):

    def get_parser_name(self):
        return 'hata'

    def get_all_last_flats(self, page_from=1, page_to=2):
        flat_links = []
        while page_from < page_to:
            response = requests.get(f"https://www.hata.by/sale-flat/page/{page_from}/", headers=HEADERS)
            html = BeautifulSoup(response.content, 'html.parser')
            for a in html.find_all("a", href=True):
                flat_links.append(a['href'])
            page_from += 1
        ready_links = list(filter(lambda el: 'object' in el, flat_links))
        return ready_links

    def enrich_links_to_flats(self, links):
        flats = []
        for counter, link in enumerate(links):
            sg.one_line_progress_meter('Лоад-бар hata.by',
                                       counter + 1, len(links),
                                       "Парсинг c hata.by",
                                       orientation='h',
                                       bar_color=('white', 'red'))
            resp = requests.get(link, headers=HEADERS)
            html = BeautifulSoup(resp.content, 'html.parser')

            '''title'''
            title = html.find('h1', class_='b-card__title').text.strip()

            '''price'''
            price = html.find('div', class_='value')
            if price is not None:
                price = int(re.sub('[^0-9]', '', price.text.strip()))
            else:
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
                square = float(re.sub('[^0-9]', '', square_rooms_info_dict['Общая площадь']))
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
                for info in html.find_all('table', class_='i-table')[3].find('a'):
                    district = info.text.strip()
                for info in html.find_all('table', class_='i-table')[4].find_all('td'):
                    micro_district = info.text.strip()
            except (Exception,):
                district = 'Не указан'
                micro_district = 'Не указан'
                # saler_phone = html.find('div', class_='p_nm', string='Телефон').find_next().text.strip()
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
                rooms_quantity=rooms_quantity
            ))
            print()
        return flats


# HataParser().update_with_last_flats()
