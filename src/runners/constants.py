from src.parsers.hata_parser import HataParser
from src.parsers.realt_parser import RealtParser

realt_parser = RealtParser()
hata_parser = HataParser()
USED_PARSERS = [realt_parser, hata_parser]