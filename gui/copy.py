# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Koki Mametani <kokimametani@gmail.com>
# License: GPLv3 or later; http://www.gnu.org/licenses/gpl.html

import gui
from gui.qt import *
from gui.utils import showCritical, showWarning


def on_copy(mw):
    gui.dialogs.open("CopyDialog", mw)


class CopyDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self._ui()
        self.show()

    def _ui(self):
        self.form = gui.forms.copydialog.Ui_CopyDialog()
        self.form.setupUi(self)
        el = self.mw.entrylist

        self.form.fromBox.addItems([key for key in el.get_config('ewkeys')])
        self.form.toBox.addItems([key for key in el.get_config('ewkeys')])
        self.form.fromBox.setCurrentText('atop')
        self.form.copyBtn.clicked.connect(self._copy)
        self.form.cancelBtn.clicked.connect(self.reject)

    def _copy(self):
        el = self.mw.entrylist
        from_ewkey = self.form.fromBox.currentText()
        to_ewkey = self.form.toBox.currentText()

        if el.count() == 0:
            showWarning("No entries found in your entry list.", title="Warnig")
            return

        if from_ewkey == to_ewkey:
            showWarning("Cannot copy the same section", title="Warning")
            return

        # Copying from and to the contents in Entry Widget
        for ew in el.get_entry_all():
            try:
                ew[to_ewkey] = ew[from_ewkey]
            except KeyError:
                pass

        # Change language mapping of the entrylist based on the copy
        el.set_config(to_ewkey, el.get_config(from_ewkey))

        el.update_all()

    def reject(self):
        self.done(0)
        gui.dialogs.close("CopyDialog")
