# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html

import gui
from gui.qt import *
from gui.utils import showCritical, showWarning, getFile, path2filename
from joytan.routine.opencsv import CsvOpenThread

# TODO: Logic for opening csv should be moved to joytan/joytan,
# and in this directory we need to implement an open dialog to
# preview csv files and give options about which columns & rows to open.


def on_open(mw):
    gui.dialogs.open("OpenDialog", mw)

class OpenDialog(QDialog):
    """
    Dialog showing some info and data to users before opening a file.
    Data may include the number of row & column of a file to open, and
    info may include a warning that too many entries slower or freeze at worst
    the app on the beta version.
    """
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.setModal(True)
        self.mw = mw
        self.path = None
        self.form = gui.forms.opendialog.Ui_OpenDialog()
        self.form.setupUi(self)

        self._ui_button()
        self._ui_progress()

        self._get_file()

        self.show()

    def _ui_button(self):
        self.form.fileBtn.clicked.connect(self._get_file)
        self.form.openBtn.clicked.connect(self._on_open)
        self.form.stopBtn.clicked.connect(self._on_stop)

    def _ui_progress(self):
        self.form.stopBtn.setEnabled(False)
        self.form.openBtn.setEnabled(True)
        self.form.progressBar.reset()
        self.form.pgMsg.setText("")

    def _on_open(self):
        if not self.path:
            showCritical("File not specified.")
            return

        self.thread = CsvOpenThread(self.path)
        self.thread.reshape.connect(lambda x: self.mw.entrylist.set_config('reshape', x))
        self.thread.new_entry.connect(self._on_progress)
        self.thread.finished.connect(self._completed)

        self.form.progressBar.setRange(0, self._count_row())
        self.form.openBtn.setEnabled(False)
        self.form.stopBtn.setEnabled(True)
        self.thread.start()

    def _on_progress(self, atop, items):
        ew = self.mw.entrylist.add_entry(atop=atop)
        ew.update_editor(items)

        self.form.pgMsg.setText("Done Entry #%d" % (ew.row + 1))
        val = self.form.progressBar.value()
        self.form.progressBar.setValue(val + 1)

    def _get_file(self):
        filter = "CSV file for Joytan EntryList (*.csv)"
        try:
            file = getFile(self.mw, "Open Existing Joytan EntryList",
                           dir=self.mw.config['workspace'], filter=filter)
            self.path = file
            self.form.fileLbl.setText(path2filename(file))
            if not file:
                return
        except:
            return

    def _on_stop(self):
        """
        TODO: Because the background thread for opening a file is too fast,
        the method to stop the thread fails to do the job although clicking the
        'stop button' quickly multiple times sometimes become successful.
        """
        if self.thread:
            self.thread.terminate()
        self._ui_progress()
        self.mw.entrylist.update_all()

    def _completed(self):
        self._ui_progress()
        self.mw.entrylist.update_all()
        self.reject()

    def _count_row(self):
        with open(self.path, encoding='utf-8') as f:
            for i, l in enumerate(f):
                pass
        return i + 1