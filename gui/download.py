import os, requests

import gui
from gui.qt import *
from gui.utils import showCritical
from emotan.downloader import Downloaders

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
        form.sourceCombo.addItems(sorted([site for site in Downloaders.keys()]))

    def start(self):
        if self.mw.entrylist.count() == 0:
            showCritical("No entries found in your entry list.", title="Error")
            return
        dler = Downloaders[self.form.sourceCombo.currentText()]()
        simpleDownload(self.mw, dler)
        self.mw.entrylist.updateAll()

    def reject(self):
        self.done(0)
        gui.dialogs.close("DownloadDialog")


def simpleDownload(mw, dler):
    mw.progress.start(min=0, max=mw.entrylist.count(), label="Start downloading", immediate=True, cancellable=True)
    for i in range(mw.entrylist.count()):
        ew = mw.entrylist.getByIndex(i + 1)
        # Don't forget to turn off 'maybeShow'. That breaks the sync of the bar and the actual progress
        mw.progress.update(label="Downloading %s from %s" %
                                 (ew.atop, dler.sourceName), maybeShow=False)
        # Don't download contents from the source you already had.
        if dler.sourceName in ew.sources:
            continue
        r = requests.get(dler.sourceUrl + ew.atop)
        items = dler.run(r.text)

        mw.entrylist.updateEntry(ew.index, items)
        ew.sources.append(dler.sourceName)
    mw.progress.finish()

