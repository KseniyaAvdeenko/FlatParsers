from abc import ABC, abstractmethod
import PySimpleGUI as sg

from src import db_client


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

    @staticmethod
    def save_flats(flats):
        for counter, flat in enumerate(flats):
            sg.one_line_progress_meter('Лоад-бар загрузки в БД',
                                       counter + 1, len(flats),
                                       "загружено в БД:",
                                       orientation='h',
                                       bar_color=('white', 'red'))
            db_client.insert_flat(flat)

    def update_with_last_flats(self, page_from=1, page_to=5):
        links = self.get_all_last_flats(page_from, page_to)
        flats = self.enrich_links_to_flats(links)
        self.save_flats(flats)