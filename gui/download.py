import requests

import gui
from gui.qt import *
from gui.utils import showCritical
from emotan.downloader import Downloaders


def on_download(mw):
    gui.dialogs.open("DownloadDialog", mw)


class DownloadDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.form = gui.forms.download.Ui_DownloadDialog()
        self.form.setupUi(self)
        self._ui()
        self.show()

    def _ui(self):
        form = self.form
        form.cancelBtn.clicked.connect(self.reject)
        form.startBtn.clicked.connect(self._download)
        form.sourceCombo.addItems(sorted([site for site in Downloaders.keys()]))

    def _download(self):
        if self.mw.entrylist.count() == 0:
            showCritical("No entries found in your entry list.", title="Error")
            return
        dler = Downloaders[self.form.sourceCombo.currentText()]()
        _simple_dl(self.mw, dler)
        self.mw.entrylist.update_all()

    def reject(self):
        self.done(0)
        gui.dialogs.close("DownloadDialog")


def _simple_dl(mw, dler):
    # Simple downloading method.
    mw.progress.start(min=0, max=mw.entrylist.count(), label="Start downloading", immediate=True, cancellable=True)
    for i in range(mw.entrylist.count()):
        ew = mw.entrylist.get_entry_at(i)
        # Don't forget to turn off 'maybeShow'. That breaks the sync of the bar and the actual progress
        mw.progress.update(label="Downloading %s from %s" %
                                 (ew.editors['atop'].text(), dler.source_name), maybeShow=False)
        # Don't download contents from the source you already had.
        if dler.source_name in ew.sources:
            continue
        r = requests.get(dler.source_url + ew.editors['atop'].text())
        items = dler.run(r.text)

        mw.entrylist.update_entry(ew.row, items)
        ew.sources.append(dler.source_name)
    mw.progress.finish()

