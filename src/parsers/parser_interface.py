# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import time

from tqdm import tqdm

from src import db_client
from progress.bar import ShadyBar


class ParserInterface(ABC):

    @abstractmethod
    def get_parser_name(self):
        return 'unnamed_parser'

    @abstractmethod
    def get_all_last_flats(self, page_from=1, page_to=2):
        return []

    @abstractmethod
    def enrich_links_to_flats(self, links: list):
        return []

    def prepare_flats_for_insert(self, flats: list):
        ready_flats = []
        for flat in flats:
            ready_flat = (flat.reference, flat.link, flat.title, flat.price, flat.price_for_meter, flat.date, flat.description, flat.square,
                          flat.city, flat.street, flat.house_number, flat.district, flat.micro_district,
                          flat.house_year,
                          flat.rooms_quantity, flat.seller_phone, ','.join(flat.images))
            ready_flats.append(ready_flat)
        return ready_flats

    # @staticmethod
    # def save_flats_1by1(flats):
    #     start_1_by_1 = time.time()
    #     for flat in tqdm(flats, desc='Загрузка в БД', colour='green', ascii=False, dynamic_ncols=True, unit=' запись',
    #                      position=0):
    #         db_client.insert_flat(flat)
    #     end_1_by_1 = time.time()
    #     with open('Estimated_time.txt', 'a') as file:
    #         file.write(f'Время затраченное на запись в БД one_record-by-one_query {len(flats)}: {end_1_by_1 - start_1_by_1}\n')

    @staticmethod
    def save_flats_many_by1(ready_flats):
            # start_many_by_1 = time.time()
            db_client.insert_many(ready_flats)
            # end_many_by_1 = time.time()
            # with open('Estimated_time.txt', 'a') as file:
            #     file.write(f'Время затраченное на запись в БД many_records-by-one_query{len(ready_flats)}: {end_many_by_1 - start_many_by_1}')

    def update_with_last_flats(self, page_from=1, page_to=5):
        links = self.get_all_last_flats(page_from, page_to)
        flats = self.enrich_links_to_flats(links)
        # self.save_flats_1by1(flats)
        self.save_flats_many_by1(self.prepare_flats_for_insert(flats))
