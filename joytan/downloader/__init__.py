# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Koki Mametani <kokimametani@gmail.com>
# License: GPLv3 or later; http://www.gnu.org/licenses/gpl.html

from joytan.downloader.dictionarycom import DictionaryComDownloader
from joytan.downloader.wiktionary import WiktionaryDownloader

Downloaders = {
    "Dictionary.com": DictionaryComDownloader,
    "Wiktionary": WiktionaryDownloader,
}
