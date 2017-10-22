import re

from bs4 import BeautifulSoup
from tools.parser.base import BaseParser

class WiktionaryParser(BaseParser):
    def __init__(self):
        BaseParser.__init__(self)
        self.source = "https://en.wiktionary.org/wiki/"