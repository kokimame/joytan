# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html

class BaseDownloader:
    """
    Experimental base class for downloader services.
    """
    SOURCE_URL = None
    SOURCE_NAME = None

    def get_url(self, query):
        """
        Make a complete URL based on given search query
        """
        raise NotImplementedError

    def run(self, data):
        """
        Each class implements a run method specific to their source.
        Download only once for an entry even if 
        Entry preference modified after the downloading session.
        """
        raise NotImplementedError