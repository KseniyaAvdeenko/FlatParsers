from src.parsers.HataParser import HataParser
from src.parsers.RealtParser import RealtParser
from src.parsers.GoHomeParser import GoHomeParser

realt_parser = RealtParser()
hata_parser = HataParser()
go_home = GoHomeParser()
USED_PARSERS = [realt_parser, go_home]

PARSE_EVERY_MINUTES = 10
POST_EVERY_MINUTES = 2
ARCHIVE = '00:00'
