from src.parsers.HataParser import HataParser
from src.parsers.RealtParser import RealtParser
from src.parsers.GoHomeParser import GoHomeParser

realt_parser = RealtParser()
hata_parser = HataParser()
go_home = GoHomeParser()
USED_PARSERS = [realt_parser, go_home]