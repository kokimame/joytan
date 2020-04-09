# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html

import gui
from gui.qt import *
from gui.utils import showCritical, showWarning, getFile, path2filename
from joytan.routine.opencsv import OpenCsvThread


def on_open(mw):
    gui.dialogs.open("OpenDialog", mw)


class OpenDialog(QDialog):
    """
    Dialog showing some info and data to users before opening a file.
    Data will include the number of row & column of a file to open, and
    info will include a warning that tells too many entries slower or freeze at worst
    the app on the beta version.
    """
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.path = None
        self.form = gui.forms.opendialog.Ui_OpenDialog()
        self.form.setupUi(self)

        self._ui_button()
        self._ui_reset()

        self._get_file()

        self.show()

    def _ui_button(self):
        self.form.fileBtn.clicked.connect(self._get_file)
        self.form.openBtn.clicked.connect(self._on_open)

    def _ui_reset(self):
        self.form.openBtn.setEnabled(True)
        self.form.fileBtn.setEnabled(True)
        self.form.progressBar.reset()
        self.form.pgMsg.setText("")

    def _on_open(self):
        if not self.path:
            showCritical("File not specified.")
            return

        self.thread = OpenCsvThread(self.path)
        self.thread.reshape.connect(lambda x: self.mw.entrylist.set_config('reshape', x))
        self.thread.new_entry.connect(self._on_progress)
        self.thread.finished.connect(self._completed)

        self.form.progressBar.setRange(0, self._count_row())
        self.form.openBtn.setEnabled(False)
        self.form.fileBtn.setEnabled(False)

        if self.form.nameCheck.isChecked():
            mpath=self.form.fileLbl.text().replace(".csv","")
            midx=mpath.find('/')
            if midx>0:
                mpath=mpath[midx+1:len(midx)-1]
            self.mw.config['title']=mpath
        self.thread.start()
        if self.form.shuffleCheck.isChecked():
            self.thread.finished.connect(lambda : self._shuffle())


    def _shuffle(self):
        targets=self.mw.entrylist.get_entry_all()
        import random
        for i in range(0, len(targets)):
            if i < len(targets) / 2:
                ew = targets[i]
                ew.move_to(targets[-i - 1].row, to_update=False)

        for i in range(0, len(targets), 2):
            ew = targets[i]
            ew.move_to(random.choice(targets).row, to_update=False)
        self.mw.entrylist.update_all()

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
        if isinstance(self.thread, OpenCsvThread):
            self.thread.to_abort()
        self._ui_reset()
        self.mw.entrylist.update_all()

    def _completed(self):
        self._ui_reset()
        self.mw.entrylist.update_all()
        self.reject()

    def _count_row(self):
        return 0
        with open(self.path, encoding='utf-8') as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def reject(self):
        self._on_stop()
        self.done(0)
        gui.dialogs.close("OpenDialog")
