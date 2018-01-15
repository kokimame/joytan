# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Koki Mametani <kokimametani@gmail.com>
# License: GPLv3 or later; http://www.gnu.org/licenses/gpl.html

from joytan.extractor.base import Extractor


class NewlineExtractor(Extractor):
    def __init__(self, file):
        Extractor.__init__(self, file)

    def _run(self):
        with open(self.file, 'r') as f:
            res = f.readlines()
        return [line.strip() for line in res]