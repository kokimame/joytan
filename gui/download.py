import os, requests

from tools.parser import Parsers
from gui.progress import ProgressDialog
from gui.utils import processCoreEvents


def onDownload(mw):
    # Look up Frame Manager of the MainWindow for the state of contents in bundles
    # to choose the right downloading method, i.e. needs to download partially or totally?
    # And also probably selecting a dictionary parser and passing it to the method,
    # which abstract parser for each downloading method sounds good.
    # - e.g partialDownload(mw, parser)
    parser = Parsers[mw.pref['onlineRef']]()
    ignorantDownload(mw, parser)
    mw.framelist._update()



def ignorantDownload(mw, parser, gstat=False):
    pd = ProgressDialog(mw.framelist.count(), msg="Downloading...")
    pd.show()

    # Fixme: Download anyway even if it's already downloaded from the same source.
    # This is why the method called ignorant.
    for i in range(mw.framelist.count()):
        # This tip probably makes pd faster to display.
        pd.setValue(i)
        processCoreEvents()

        bw = mw.framelist.getBundleWidget(i)
        if parser.source in bw.bundle.sources:
            continue
        r = requests.get(parser.source + bw.bundle.name)
        data = r.text
        items = parser.run(data)

        mw.framelist.updateBundle(bw.bundle.name, items)
        bw.bundle.sources.append(parser.source)

def downloadGstaticSound(word, filename):
    url = "http://ssl.gstatic.com/dictionary/static/sounds/oxford/"
    gb1 = "--_gb_1.mp3"  # A trailing type for gstatic dictionary
    gb18 = "--_gb_1.8.mp3"  # A trailing type for gstatic dictionary

    for w_key in [word + gb1, word + gb18, "x" + word + gb18]:
        r = requests.get(url + w_key, stream=True)
        if r.ok:
            break
        elif w_key == "x" + word + gb18 and not r.ok:
            raise Exception("Audio for '" + word + "' not found")

    with open(filename, "wb") as f:
        f.write(r.content)
