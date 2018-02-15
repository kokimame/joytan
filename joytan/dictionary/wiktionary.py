# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html

import re

from bs4 import BeautifulSoup
from joytan.dictionary.base import BaseDownloader

class WiktionaryDownloader(BaseDownloader):
    """
    Provides an interface to fetch dictionary entries from Wiktionary
    """

    SOURCE_URL = "https://en.wiktionary.org/wiki/"
    SOURCE_NAME = "Wiktionary"

    def __init__(self):
        BaseDownloader.__init__(self)

    def get_url(self, query):
        if not query:
            return ''
        return self.SOURCE_URL + query

    def run(self, html):
        soup = BeautifulSoup(html, "html.parser")
        ols = soup.find('ol')

        if ols:
            items = {}
            for i, content in enumerate(ols.find_all('li', recursive=False)):
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
        else:
            return {}