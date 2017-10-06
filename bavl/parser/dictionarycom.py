import re

from bs4 import BeautifulSoup
from bavl.parser.base import BaseParser

class DictionaryComParser(BaseParser):
    def __init__(self):
        BaseParser.__init__(self)

    def run(self, data):
        bitems = []
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
            except ValueError:
                define, examp = defc, ""
                define = define.strip()
            bitems.append({'define': define, 'examples': [examp]})

            """
            Bundle item format (temporally)
            {
                'define' : 'a definition of a word'
                'examples' : ['a example for the definition', 'another example', ...]
            }
            
            """

        return bitems