import re
import requests
from datetime import datetime
import PySimpleGUI as sg
from bs4 import BeautifulSoup
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
            for a in html.find_all("a", href=True, class_='teaser-title'):
                flat_links.append(a['href'])
            page_from += 1
        ready_links = list(filter(lambda el: 'object' in el, flat_links))
        return ready_links

    def enrich_links_to_flats(self, links):
        flats = []
        for counter, link in enumerate(links):
            sg.one_line_progress_meter('Лоад-бар realt.by',
                                       counter + 1, len(links),
                                       "Парсинг c realt.by",
                                       orientation='h',
                                       bar_color=('white', 'red'))
            response = requests.get(link, headers=HEADERS)
            html = BeautifulSoup(response.content, 'html.parser')
            '''title'''
            title = html.find('h1', class_='order-1').text.strip()
            '''price'''
            price = html.find('h2', class_='w-full')
            if price is not None:
                price = int(re.sub('[^0-9]', '', price.text.strip()))
            else:
                price = 0

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
                square = float(re.sub('[^0-9|,]', '', info_dict['Площадь общая']))
                rooms_quantity = int(info_dict['Количество комнат'])
                house_year = int(info_dict['Год постройки'])
            except (Exception,):
                rooms_quantity = 0
                square = 0
                house_year = 0

            '''location: city, street, house_number, district, micro_district'''
            try:
                location_info_list = []
                location_info_values_list = []
                for info in html.find('ul', class_='w-full mb-0.5 -my-1').find_all('span'):
                    if info.text == 'Номер дома':
                        continue
                    else:
                        loc_info_keys = info.text
                        location_info_list.append(loc_info_keys)
                for info in html.find('ul', class_='w-full mb-0.5 -my-1').find_all('a'):
                    info_values = re.sub("[\n|\xa0]", "", info.text.strip())
                    location_info_values_list.append(info_values)
                for p in html.find('ul', class_='w-full mb-0.5 -my-1').find_all('p'):
                    house_number = p.text

                info_location_dict = dict(zip(location_info_list, location_info_values_list))
                city = info_location_dict['Населенный пункт']
                street = info_location_dict['Улица']
                district = info_location_dict['Район города']
                micro_district = info_location_dict['Микрорайон']
            except (Exception,):
                city = 'Не указан'
                street = 'Не указан'
                micro_district = 'Не указан'
                house_number = 'Не указан'
                district = 'Не указан'

            '''date'''
            try:
                date = datetime.strptime(html.find('span', class_='mr-1.5').text.strip(), '%d.%m.%Y')
            except (Exception,):
                date = datetime.now()

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
                rooms_quantity=rooms_quantity
            ))
        return flats


# RealtParser().update_with_last_flats(1, 5)
