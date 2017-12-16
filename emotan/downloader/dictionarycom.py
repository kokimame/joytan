import re

from bs4 import BeautifulSoup
from emotan.downloader.base import BaseDownloader

class DictionaryComDownloader(BaseDownloader):
    def __init__(self):
        BaseDownloader.__init__(self)
        self.sourceUrl = "http://dictionary.com/browse/"
        self.sourceName = "Dicitionary.com"

    def run(self, data):
        defex = []
        soup = BeautifulSoup(data, "html.parser")
        defcs = soup.find_all(attrs={"class": "def-content"})

        # First, remove all HTML elements with <> and escape sequences \r and \n,
        # and then split strings at whitespace and join them with a single whitespace.
        defcs = [' '.join(re.sub('\<.*\>', '', defc.text.strip()
                    .replace('\r', '').replace('\n', '')).split()) for defc in defcs]

        for n, defc in enumerate(defcs):
            try:
                define, examp = defc.split(":")
                define = define.strip()
                examp = examp.strip()
            except ValueError: # If definition has no example
                define, examp = defc, ""
                define = define.strip()
            defex.append({'define': define, 'examples': [examp]})

            """
            Entry item format (temporally)
            {
                'define' : 'a definition of a word'
                'examples' : ['a example for the definition', 'another example', ...]
            }
            
            """

        return defex