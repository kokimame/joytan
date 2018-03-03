# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html


import requests

import gui
from gui.qt import *
from gui.utils import showCritical
from joytan.dictionary import DictionaryService


def on_lookup(mw):
    gui.dialogs.open("LookupDialog", mw)


class LookupThread(QThread):

    prog = pyqtSignal(str)
    step = pyqtSignal(int, dict)

    def __init__(self, targets, service):
        QThread.__init__(self)
        self.targets = targets
        self.service = service

    def run(self):
        for ew in self.targets:
            if not ew['atop']:
                continue
            self.prog.emit(ew['atop'])
            r = requests.get(self.service.make_url(ew['atop']))
            items = self.service.run(r.text)
            self.step.emit(ew.row, items)
        self.quit()


class LookupDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        # Download thread
        self.lt = None
        self.form = gui.forms.lookup.Ui_LookupDialog()
        self.form.setupUi(self)
        self._ui()
        self.show()

    def _ui(self):
        form = self.form
        form.cancelBtn.setDisabled(True)
        form.cancelBtn.clicked.connect(self._thread_stop)
        form.startBtn.clicked.connect(self._lookup)
        form.sourceCombo.addItems(sorted([site for site in DictionaryService.keys()]))

    def _lookup(self):
        if self.mw.entrylist.count() == 0:
            showCritical("No entries found in your entry list.", title="Error")
            return

        source_name = self.form.sourceCombo.currentText()
        service = DictionaryService[source_name]()

        if self.form.onlyCheck.isChecked():
            targets = self.mw.entrylist.get_entry_selected()
        else:
            targets = self.mw.entrylist.get_entry_all()
        self.form.progressBar.setRange(0, len(targets))

        def _on_progress(name):
            self.form.pgMsg.setText("Looking up %s." % name)
            val = self.form.progressBar.value()
            self.form.progressBar.setValue(val+1)

        self.lt = LookupThread(targets, service)
        self.lt.prog.connect(_on_progress)
        self.lt.step.connect(self.mw.entrylist.update_entry)
        self._thread_start()
        self.lt.finished.connect(self.reject)

    def _thread_start(self):
        self.form.startBtn.setDisabled(True)
        self.lt.start()
        self.form.cancelBtn.setEnabled(True)

    def _thread_stop(self):
        if self.lt:
            self.lt.terminate()
            self.form.startBtn.setEnabled(True)
            self.form.cancelBtn.setDisabled(True)

    def reject(self):
        self.form.startBtn.setEnabled(True)
        self.form.cancelBtn.setDisabled(True)
        self.mw.entrylist.update_all()
        self.done(0)
        gui.dialogs.close("LookupDialog")


