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
        self.form = gui.forms.sortdialog.Ui_SortDialog()
        self.form.setupUi(self)

        self._ui_progress()
        self._ui_others()

        self.show()

    def _ui_others(self):
        self.form.ewkeyBox.addItems([key for key in self.el.get_config('ewkeys')])
        self.form.optionBox.currentTextChanged.connect(self._on_option_changed)
        self.form.okBtn.clicked.connect(self._on_ok)
        self._on_option_changed(self.form.optionBox.currentText())

    def _ui_progress(self):
        self.form.okBtn.setEnabled(True)
        self.form.progressBar.reset()
        self.form.pgMsg.setText("")

    def _on_option_changed(self, new_option):
        """
        Disable 'sort-by' combobox if new sorting option doesn't use it. 
        """
        with_sort_by = []
        if new_option in with_sort_by:
            self.form.ewkeyBox.setDisabled(False)
        else:
            self.form.ewkeyBox.setDisabled(True)

    def _on_ok(self):
        if self.el.count() == 0:
            self.reject()
            return
        self.setModal(True)

        sort_opt = self.form.optionBox.currentText()
        focus_key = self.form.ewkeyBox.currentText()
        if self.form.onlyCheck.isChecked():
            entries = self.el.get_entry_selected()
        else:
            entries = self.el.get_entry_all()

        if sort_opt == 'Shuffle':
            self._on_shuffle(entries)
        elif sort_opt == "Reverse":
            self._on_reverse(entries)

        self.reject()

    def _on_shuffle(self, targets):
        self.form.progressBar.setRange(0, len(targets))
        import random
        for i in range(0, len(targets)):
            if i < len(targets) / 2:
                ew = targets[i]
                ew.move_to(targets[-i - 1].row, to_update=False)
                self._on_progress(1)

        for i in range(0, len(targets), 2):
            ew = targets[i]
            ew.move_to(random.choice(targets).row, to_update=False)
            self._on_progress(1)
        self.el.update_all()

    def _on_reverse(self, targets):
        length = len(targets)
        self.form.progressBar.setRange(0, length/2)
        for i in range(0, length):
            if i == length - i - 1 or i == length / 2:
                break
            else:
                # One step to reverse the EntryList by swapping two Entries.
                # TODO: Implement swapping method in EntryList class.
                top, bottom = targets[i].row, targets[-i - 1].row
                targets[-i - 1].move_to(top, to_update=False)
                targets[i].move_to(bottom, to_update=False)
            self._on_progress(1)

        self.el.update_all()

    def _on_progress(self, step):
        val = self.form.progressBar.value()
        self.form.progressBar.setValue(val + step)

    def reject(self):
        self._ui_progress()
        self.done(0)
        gui.dialogs.close("CopyDialog")
