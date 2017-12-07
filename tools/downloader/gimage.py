# coding: utf-8

import os
import time
import requests

keywords = ['happy', 'sad', 'angry', 'love']

size = {'medium': '&tbs=islt:vga,isz:m',
        'icon': '&tbs=isz:i'}

HEADERS = {"User-Agent":
               "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) "\
               + "Chrome/41.0.2228.0 Safari/537.36"}
URL = 'https://www.google.com/search?q={keyword}&espv=2&biw=1366&bih=667&site=webhp&source=lnms'\
      + size['medium'] + '&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
MAXIMG = 5

from PyQt5.QtCore import QThread
class GimageThread(QThread):
    def __init__(self, keyword, destDir):
        QThread.__init__(self)
        self.keyword = keyword
        self.destDir = destDir

    def run(self):
        downloadImages(self.keyword, self.destDir)
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


def downloadImages(keyword, destDir):
    start = time.time()
    links = []
    iteration = "Search = " + keyword
    print(iteration)
    print("Evaluating...")
    # make a search keyword  directory
    if os.path.isdir(destDir):
        import shutil
        shutil.rmtree(destDir)
    os.makedirs(destDir)

    url = URL.format(keyword=keyword)
    raw_html = (downloadPage(url))
    time.sleep(0.1)
    links = links + (_getAllLinks(raw_html, max=5))

    total_time = time.time() - start
    print("Total time taken: %.2f Seconds" % total_time)
    print("Total Image Links = " + str(len(links)))
    print("Starting Download...")

    for j, link in enumerate(links[:MAXIMG]):
        try:
            req = requests.get(link, headers=HEADERS)
            imgfile = os.path.join(destDir, str(j + 1) + ".jpg")
            output_file = open(imgfile, 'wb')

            # Save the actual image
            output_file.write(req.content)
            print("completed ====> " + str(j + 1) + " (%.3fMB)" % float(len(req.content)/1000000))

        except (IOError, requests.HTTPError, requests.ConnectionError) as e:
            print(e)
    print("= Done =\n")
