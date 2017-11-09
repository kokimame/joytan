import os, requests

import gui
from gui.qt import *
from tools.parser import Parsers

def onDownload(mw):
    gui.dialogs.open("DownloadDialog", mw)

class DownloadDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.form = gui.forms.download.Ui_DownloadDialog()
        self.form.setupUi(self)
        self.setupWidgets()
        self.show()

    def setupWidgets(self):
        form = self.form
        form.cancelBtn.clicked.connect(self.reject)
        form.startBtn.clicked.connect(self.start)
        form.sourceCombo.addItems(sorted([site for site in Parsers.keys()]))
        form.sourceCombo.setCurrentText(self.mw.pref["onlineSrc"])

    def start(self):
        parser = Parsers[self.form.sourceCombo.currentText()]()
        simpleDownload(self.mw, parser)
        self.mw.framelist._update()

    def reject(self):
        self.done(0)
        gui.dialogs.close("DownloadDialog")


def simpleDownload(mw, parser):
    mw.progress.start(min=0, max=mw.framelist.count(), label="Start downloading", immediate=True, cancellable=True)
    for i in range(mw.framelist.count()):
        bw = mw.framelist.getBundleWidget(i)
        # Don't forget to turn off 'maybeShow'. That breaks the sync of the bar and the actual progress
        mw.progress.update(label="Downloading %s from %s" %
                                 (bw.name, parser.sourceName), maybeShow=False)
        # Don't download contents from the source you already had.
        if parser.sourceName in bw.sources:
            continue
        r = requests.get(parser.sourceUrl + bw.name)
        data = r.text
        items = parser.run(data)

        mw.framelist.updateBundle(bw.name, items)
        bw.sources.append(parser.sourceName)
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
