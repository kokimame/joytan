# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html

import gui
from gui.qt import *
from gui.utils import showCritical


def on_sort(mw):
    gui.dialogs.open("SortDialog", mw)


class SortDialog(QDialog):

    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.el = mw.entrylist
        self._ui()
        self.show()

    def _ui(self):
        self.form = gui.forms.sortdialog.Ui_SortDialog()
        self.form.setupUi(self)
        self.form.ewkeyBox.addItems([key for key in self.el.get_config('ewkeys')])
        self.form.okBtn.clicked.connect(self._on_ok)

    def _on_ok(self):
        if self.el.count() == 0:
            self.reject()
            return
        sort_opt = self.form.sortBox.currentText()
        focus_key = self.form.ewkeyBox.currentText()
        if self.form.onlyCheck.isChecked():
            to_sort = self.el.get_entry_selected()
        else:
            to_sort = self.el.get_entry_all()

        if sort_opt == 'Shuffle':
            self._on_shuffle(to_sort)
        elif sort_opt == "Reverse":
            self._on_reverse(to_sort)

        self.reject()

    def _on_shuffle(self, targets):
        import random
        for ew in targets:
            ew.move_to(random.choice(targets).row)

    def _on_reverse(self, targets):
        length = len(targets)
        for i in range(0, length):
            if i == length - i - 1 or i == length / 2:
                break
            else:
                top, bottom = targets[i].row, targets[-i - 1].row
                targets[-i - 1].move_to(top)
                targets[i].move_to(bottom)

    def reject(self):
        self.done(0)
        gui.dialogs.close("CopyDialog")
