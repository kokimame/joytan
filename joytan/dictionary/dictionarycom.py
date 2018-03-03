# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html

import re

from bs4 import BeautifulSoup
from joytan.dictionary.base import BaseDictionary

class DictionaryCom(BaseDictionary):
    """
    Provides an interface to fetch dictionary entries from Dictionary.com
    """

    SOURCE_URL = "http://dictionary.com/browse/"
    SOURCE_NAME = "Dicitionary.com"

    def __init__(self):
        BaseDictionary.__init__(self)

    def make_url(self, query):
        return self.SOURCE_URL + query

    def run(self, html):
        soup = BeautifulSoup(html, "html.parser")
        defexs = soup.find_all(attrs={"class": "def-content"})

        # First, remove all HTML elements with <> and escape sequences \r and \n,
        # and then split strings at whitespace and join them with a single whitespace.
        defexs = [' '.join(re.sub('\<.*\>', '', d.text.strip()
                    .replace('\r', '').replace('\n', '')).split()) for d in defexs]

        items = {}
        for i, defex in enumerate(defexs):
            try:
                define, ex = defex.split(":")
                define = define.strip()
                ex = ex.strip()
            except ValueError: # If definition has no example
                define, ex = defex, ""
                define = define.strip()
            items['def-%d' % (i + 1)] = define
            items['ex-%d-1' % (i + 1)] = ex

        return items