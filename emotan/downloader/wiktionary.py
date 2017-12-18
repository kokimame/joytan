import re

from bs4 import BeautifulSoup
from emotan.downloader.base import BaseDownloader

class WiktionaryDownloader(BaseDownloader):
    def __init__(self):
        BaseDownloader.__init__(self)
        self.sourceUrl = "https://en.wiktionary.org/wiki/"
        self.sourceName = "Wiktionary"

    def run(self, data):
        # Dictionary which stores definition and example
        items = {}
        soup = BeautifulSoup(data, "html.parser")
        table = soup.find('ol')

        for i, content in enumerate(table.find_all('li', recursive=False)):
            examples = []
            for trash in content.find_all('ul'):
                trash.replaceWith('')
            for example in content.find_all('dl'):
                examples.append(example.text)
                # Remove stored example from definition text
                example.replaceWith('')
            if len(examples) == 0:
                examples = ['']
            items['def-%d' % (i + 1)] = content.text
            for j, ex in enumerate(examples):
                items['ex-%d-%d' % (i + 1, j + 1)] = ex

        return items