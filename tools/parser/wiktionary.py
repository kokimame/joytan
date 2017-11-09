import re

from bs4 import BeautifulSoup
from tools.parser.base import BaseParser

class WiktionaryParser(BaseParser):
    def __init__(self):
        BaseParser.__init__(self)
        self.sourceUrl = "https://en.wiktionary.org/wiki/"
        self.sourceName = "Wiktionary"

    def run(self, data):
        # Dictionary which stores definition and example
        defex = []
        soup = BeautifulSoup(data, "html.parser")
        table = soup.find('ol')

        for content in table.find_all('li', recursive=False):
            examples = []
            for trash in content.find_all('ul'):
                trash.replaceWith('')
            for example in content.find_all('dl'):
                examples.append(example.text)
                # Remove stored example from definition text
                example.replaceWith('')
            if len(examples) == 0:
                examples = ['']
            defex.append({'define': content.text, 'examples':examples})

        return defex