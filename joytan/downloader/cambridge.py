# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Koki Mametani <kokimametani@gmail.com>
# License: GPLv3 or later; http://www.gnu.org/licenses/gpl.html

from joytan.downloader.base import BaseDownloader

class CambridgeDownloader(BaseDownloader):
    def __init__(self):
        BaseDownloader.__init__()
        self.source_url = "http://dictionary.cambridge.org/dictionary/english/"
        self.source_name = "Cambridge Dictionary"