# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Koki Mametani <kokimametani@gmail.com>
# License: GPLv3 or later; http://www.gnu.org/licenses/gpl.html

from joytan.extractor.newline import NewlineExtractor

Extractors = (
    ("DSV format - Words separated by newline (*.dsv *.txt)", NewlineExtractor),
)