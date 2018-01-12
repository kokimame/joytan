import requests

import gui
from gui.qt import *
from gui.utils import showCritical
from joytan.downloader import Downloaders


def on_download(mw):
    gui.dialogs.open("DownloadDialog", mw)


class DownloadThread(QThread):

    prog = pyqtSignal(str)
    step = pyqtSignal(int, dict)

    def __init__(self, targets, loader):
        QThread.__init__(self)
        self.targets = targets
        self.loader = loader

    def run(self):
        for ew in self.targets:
            self.prog.emit(ew['atop'])
            r = requests.get(self.loader.source_url + ew['atop'])
            items = self.loader.run(r.text)
            self.step.emit(ew.row, items)
        self.quit()


class DownloadDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        # Download thread
        self.dt = None
        self.form = gui.forms.download.Ui_DownloadDialog()
        self.form.setupUi(self)
        self._ui()
        self.show()

    def _ui(self):
        form = self.form
        form.cancelBtn.setDisabled(True)
        form.cancelBtn.clicked.connect(self._thread_stop)
        form.startBtn.clicked.connect(self._download)
        form.sourceCombo.addItems(sorted([site for site in Downloaders.keys()]))

    def _download(self):
        if self.mw.entrylist.count() == 0:
            showCritical("No entries found in your entry list.", title="Error")
            return

        loader = Downloaders[self.form.sourceCombo.currentText()]()\

        if self.form.onlyCheck.isChecked():
            targets = self.mw.entrylist.get_entry_selected()
        else:
            targets = self.mw.entrylist.get_entry_all()
        self.form.progressBar.setRange(0, len(targets))

        def _on_progress(name):
            self.form.pgMsg.setText("Downloading %s." % name)
            val = self.form.progressBar.value()
            self.form.progressBar.setValue(val+1)

        self.dt = DownloadThread(targets, loader)
        self.dt.prog.connect(_on_progress)
        self.dt.step.connect(self.mw.entrylist.update_entry)
        self._thread_start()
        self.dt.finished.connect(self.reject)

    def _thread_start(self):
        self.form.startBtn.setDisabled(True)
        self.dt.start()
        self.form.cancelBtn.setEnabled(True)

    def _thread_stop(self):
        if self.dt:
            self.dt.terminate()
            self.form.startBtn.setEnabled(True)
            self.form.cancelBtn.setDisabled(True)

    def reject(self):
        self.form.startBtn.setEnabled(True)
        self.form.cancelBtn.setDisabled(True)
        self.mw.entrylist.update_all()
        self.done(0)
        gui.dialogs.close("DownloadDialog")


