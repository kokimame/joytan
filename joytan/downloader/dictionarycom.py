# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Koki Mametani <kokimametani@gmail.com>
# License: GPLv3 or later; http://www.gnu.org/licenses/gpl.html

import re

from bs4 import BeautifulSoup
from joytan.downloader.base import BaseDownloader

class DictionaryComDownloader(BaseDownloader):
    def __init__(self):
        BaseDownloader.__init__(self)
        self.source_url = "http://dictionary.com/browse/"
        self.source_name = "Dicitionary.com"

    def run(self, data):
        items = {}
        soup = BeautifulSoup(data, "html.parser")
        defexs = soup.find_all(attrs={"class": "def-content"})

        # First, remove all HTML elements with <> and escape sequences \r and \n,
        # and then split strings at whitespace and join them with a single whitespace.
        defexs = [' '.join(re.sub('\<.*\>', '', d.text.strip()
                    .replace('\r', '').replace('\n', '')).split()) for d in defexs]

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