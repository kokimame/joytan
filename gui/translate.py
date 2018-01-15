# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Koki Mametani <kokimametani@gmail.com>
# License: GPLv3 or later; http://www.gnu.org/licenses/gpl.html

import gui
from gui.qt import *
from gui.utils import showCritical

from googletrans import Translator
from googletrans.constants import LANGCODES


def on_translate(mw):
    gui.dialogs.open("TranslateDialog", mw)


class TranslateThread(QThread):

    prog = pyqtSignal(str)
    step = pyqtSignal(int, dict)

    def __init__(self, targets, group, destcode):
        QThread.__init__(self)
        self.targets = targets
        self.group = group
        # Destination language to translate into
        self.translate = lambda text: Translator().translate(text, dest=destcode).text

    def run(self):
        for ew in self.targets:
            items = {}
            self.prog.emit(ew['atop'])
            if 'atop' in self.group:
                items['atop'] = self.translate(ew['atop'])

            for i in range(1, ew.ndef + 1):
                ewkey = 'def-%d' % i
                if ewkey in self.group and ew[ewkey] != '':
                    items['def-%d' % i] = self.translate(ew[ewkey])

                for j in range(1, ew.nex + 1):
                    ewkey = 'ex-%d-%d' % (i, j)
                    if ewkey in self.group and ew[ewkey] != '':
                        items['ex-%d-%d' % (i, j)] = self.translate(ew[ewkey])

            self.step.emit(ew.row, items)

        self.quit()


class TranslateDialog(QDialog):

    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self._ui()
        self.show()

    def _ui(self):
        self.form = gui.forms.translate.Ui_TranslateDialog()
        self.form.setupUi(self)
        # Setup combo box for languages
        self.form.langCombo.addItems(sorted([lang.title() for lang in LANGCODES.keys()]))
        self.form.langCombo.setCurrentText("Japanese")
        self.form.cancelBtn.clicked.connect(self._thread_stop)
        self.form.startBtn.clicked.connect(self._translate)

        _list = self.form.keyList
        # Add checkbox corresponding to each ewkey of Entry
        for ewkey in self.mw.entrylist.get_config('ewkeys'):
            check = QCheckBox(ewkey)
            lwi = QListWidgetItem()
            lwi.setSizeHint(check.sizeHint())
            _list.addItem(lwi)
            _list.setItemWidget(lwi, check)


    # Start translation
    def _translate(self):
        if self.mw.entrylist.count() == 0:
            showCritical("No entries found in your entry list.", title="Error")
            return

        ewkeys = []
        # Get language code of target language to translate to from the library
        destcode = LANGCODES[self.form.langCombo.currentText().lower()]
        # Check which section to translate
        _list = self.form.keyList
        for i in range(_list.count()):
            ch = _list.itemWidget(_list.item(i))
            if ch.isChecked():
                ewkeys.append(ch.text())

        if self.form.onlyCheck.isChecked():
            targets = self.mw.entrylist.get_entry_selected()
        else:
            targets = self.mw.entrylist.get_entry_all()
        self.form.progressBar.setRange(0, len(targets))

        def _on_progress(name):
            self.form.pgMsg.setText("Translating %s." % name)
            val = self.form.progressBar.value()
            self.form.progressBar.setValue(val+1)

        self.tt = TranslateThread(targets, ewkeys, destcode)
        self.tt.prog.connect(_on_progress)
        self.tt.step.connect(self.mw.entrylist.update_entry)
        self._thread_start()
        self.tt.finished.connect(self.reject)

    def _thread_start(self):
        self.form.startBtn.setDisabled(True)
        self.tt.start()
        self.form.cancelBtn.setEnabled(True)

    def _thread_stop(self):
        if self.tt:
            self.tt.terminate()
            self.form.startBtn.setEnabled(True)
            self.form.cancelBtn.setDisabled(True)

    def reject(self):
        self.mw.entrylist.update_all()
        self.done(0)
        gui.dialogs.close("TranslateDialog")
