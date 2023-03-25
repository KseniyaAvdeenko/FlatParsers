# -*- coding: utf-8 -*-
import traceback
from abc import ABC, abstractmethod
from src.db_clients import db_client_parsers
from src.sentry_logging.base_logging import *
from src.sentry_logging.sentry_parsers_logger import *

logger = logging.getLogger(__name__)


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
            ready_flat = (
                flat.reference, flat.link, flat.title, flat.price, flat.price_for_meter, flat.date, flat.description,
                flat.square,
                flat.city, flat.street, flat.house_number, flat.district, flat.micro_district,
                flat.house_year,
                flat.rooms_quantity, flat.seller_phone, ','.join(flat.images))
            ready_flats.append(ready_flat)
        return ready_flats

    @staticmethod
    def save_flats_many_by1(ready_flats):
        db_client_parsers.insert_many(ready_flats)

    def update_with_last_flats(self, page_from=1, page_to=5):
        try:
            logger.info(f'Function (make_post_archived) is started')
            links = self.get_all_last_flats(page_from, page_to)
            flats = self.enrich_links_to_flats(links)
            self.save_flats_many_by1(self.prepare_flats_for_insert(flats))
        except (Exception,):
            logger.exception('Exception is occurred', {traceback.format_exc()})
