# coding: utf-8

import os
import time
import requests
import re


SIZE = {'medium': '&tbs=islt:vga,isz:m',
        'icon': '&tbs=isz:i'}
HEADERS = {"User-Agent":
               "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) "\
               + "Chrome/41.0.2228.0 Safari/537.36"}
URL = 'https://www.google.com/search?q={keyword}&espv=2&biw=1366&bih=667&site=webhp&source=lnms'\
      + SIZE['medium'] + '&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'


from PyQt5.QtCore import QThread, pyqtSignal

class GimageThread(QThread):
    sig = pyqtSignal(str)

    def __init__(self, keyword, destDir, maxImg):
        QThread.__init__(self)
        self.keyword = keyword
        self.destDir = destDir
        self.maxImg = maxImg
        self.url = None
        self.links = []

    def run(self):
        if not self.url:
            self.url = URL.format(keyword=self.keyword)
            raw_html = (downloadPage(self.url))
            self.links += (_getAllLinks(raw_html, max=15))

            if os.path.isdir(self.destDir):
                import shutil
                shutil.rmtree(self.destDir)
            os.makedirs(self.destDir)

        i, upcnt = 0, 0
        while True:
            link = self.links[i]
            imgfile = downloadImage(link, os.path.join(self.destDir, str(i)))
            if imgfile:
                self.sig.emit(imgfile)
                upcnt += 1
            if upcnt >= self.maxImg:
                break
            i += 1
            time.sleep(0.1)

        self.quit()


# Downloading entire Web Document (Raw Page Content)
def downloadPage(url):
    try:
        req = requests.get(url, headers=HEADERS)
        respData = req.text
        return respData
    except Exception as e:
        print(str(e))

# Finding 'Next Image' from the given raw page
def _getNextLink(s):
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


# Getting all links with the help of '_images_get_next_image'
def _getAllLinks(page, max=10):
    links = []
    while True:
        link, end_content = _getNextLink(page)
        if link == "no_links" or len(links) >= max:
            break
        else:
            links.append(link)
            # Ethically slow down downloading in respect to the site owner
            time.sleep(0.1)
            page = page[end_content:]
    return links


def downloadImage(link, piwoe):
    # link: URL of the image
    # piwoe: Path to image file without extension
    try:
        # Filtering image files with extension any other than jpeg, jpg and png
        ff = None
        for chunk in re.split(':|/|\.|\?', link):
            if chunk in ['jpeg', 'jpg', 'png']:
                ff = chunk
                break
        if not ff:
            return None

        req = requests.get(link, headers=HEADERS)
        imgfile = os.path.join(piwoe + "." + ff)
        output_file = open(imgfile, 'wb')

        # Save the actual image
        output_file.write(req.content)
        print("completed ====> " + imgfile + " (%.3fMB)" % float(len(req.content) / 1000000))
        return imgfile

    except (IOError, requests.HTTPError, requests.ConnectionError) as e:
        print(e)

