# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html

import os
import time
import requests
import re

from gui.qt import *
from gui.utils import path_temp

# The User-Agent of our requests
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/41.0.2228.0 Safari/537.36"}

# Base URL to access Google Image with a few of arguments.
# keyword: Search query.
# size: Image size
# TODO: Support more args, such as Color, Usage rights etc.
BASE_URL = 'https://www.google.com/search?q={keyword}' \
           '&espv=2&biw=1366&bih=667&site=webhp&source=lnms' \
           '{size}&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'

# Image size.
SIZE = {'medium': '&tbs=islt:vga,isz:m',
        'icon': '&tbs=isz:i'}

# Valid image file extension
# .gif, .svg etc are not supported
VALID_EXT = ['jpeg', 'jpg', 'png']


class GimageThread(QThread):
    """
    Thread class to retrieves links in Google Image search results and 
    downloads images from the source links to local computer.
    On success, return the path of a downloaded image to User Interface
    via 'upload' signal.
    NOTE: On deciding the speed of the request, consider the fact that 
    this thread will be executed in parallel
    """

    upload = pyqtSignal(str, str)

    def __init__(self, keyword, destdir):
        QThread.__init__(self)
        self.keyword = keyword
        self.destdir = destdir
        self.img_total = 0
        self.url = None
        self.links = []

    def update_keyword(self, keyword):
        """
        Update keyword (search query), resetting URL of Google Image search 
        """
        self.keyword = keyword
        self.url = None

    def run(self):
        """
        The entry point of this thread.
        The method downloads as much images as possible under the number
        externally specified by set_total().
        """
        if not self.url:
            self.url = BASE_URL.format(keyword=self.keyword, size=SIZE['medium'])
            raw_html = (download_page(self.url))
            self.links  = _get_all_links(raw_html, max=15)

        if not os.path.exists(self.destdir):
            os.makedirs(self.destdir)

        i, uploads = 0, 0
        while i < len(self.links):
            link = self.links[i]
            imgfile = download_image(link, os.path.join(path_temp(self.destdir)))
            if imgfile:
                self.upload.emit(imgfile, link)
                self.links.remove(link)
                uploads += 1
            if uploads >= self.img_total:
                break
            i += 1
            # The rest between
            time.sleep(0.1)

        self.quit()

    def set_total(self, n):
        """
        Set the maximum number of images to download at once. 
        """
        self.img_total = n


def download_page(url):
    """
    Downloading entire Web Document (Raw Page Content) 
    """
    try:
        req = requests.get(url, headers=HEADERS)
        resp_data = req.text
        return resp_data
    except Exception as e:
        print(str(e))


def _get_next_link(s):
    """
    Finding 'Next Image' from the given raw page 
    """
    start_line = s.find('rg_di')
    if start_line == -1:  # If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"', start_line + 1)
        end_content = s.find(',"ow"', start_content + 1)
        content_raw = str(s[start_content + 6:end_content - 1])
        return content_raw, end_content


def _get_all_links(page, max=10):
    """
    Getting all links with the help of '_images_get_next_image' 
    """
    links = []
    while True:
        link, end_content = _get_next_link(page)
        if link == "no_links" or len(links) >= max:
            break
        else:
            links.append(link)
            # Ethically slow down downloading in respect to the site owner
            time.sleep(0.1)
            page = page[end_content:]
    return links


def download_image(link, path_no_ext):
    """
    :param link: Link to an image
    :param path_no_ext: Path to image file without extension 
    :return: Path to the downloaded image in local
    
    Download image from a given link
    """
    try:
        # Filtering image files with extension any other than VALID_EXT
        ff = None
        for chunk in re.split(':|/|\.|\?', link):
            if chunk in VALID_EXT:
                ff = chunk
                break
        if not ff:
            return None

        req = requests.get(link, headers=HEADERS)
        imgfile = os.path.join(path_no_ext + "." + ff)
        output_file = open(imgfile, 'wb')

        # Save the actual image
        output_file.write(req.content)
        #print("completed ====> " +
        #      imgfile + " (%.3fMB)" % float(len(req.content) / 1000000))

        output_file.close()
        return imgfile

    except Exception as e:
        # Like (IOError, requests.HTTPError,
        # requests.ConnectionError, UnicodeError)
        # Exception while downloading is ok to be ignored and just proceed to next session
        #
        pass

