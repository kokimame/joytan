import os, requests

from tools.parser import Parsers

def onDownload(mw):
    parser = Parsers[mw.pref['onlineRef']]()
    simpleDownload(mw, parser)
    mw.framelist._update()



def simpleDownload(mw, parser):
    mw.progress.start(min=0, max=mw.framelist.count(), label="Start downloading", immediate=True, cancellable=True)
    for i in range(mw.framelist.count()):
        bw = mw.framelist.getBundleWidget(i)
        # Don't forget to turn off 'maybeShow'. That breaks the sync of the bar and the actual progress
        mw.progress.update(label="Downloading %s" % bw.name, maybeShow=False)
        # Don't download contents from the source you already had.
        if parser.source in bw.sources:
            continue
        r = requests.get(parser.source + bw.name)
        data = r.text
        items = parser.run(data)

        mw.framelist.updateBundle(bw.name, items)
        bw.sources.append(parser.source)
    mw.progress.finish()

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
