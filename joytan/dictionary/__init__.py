# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html

from joytan.dictionary.dictionarycom import DictionaryCom
from joytan.dictionary.wiktionary import Wiktionary

DictionaryService = {
    "Dictionary.com": DictionaryCom,
    "Wiktionary": Wiktionary,
}
