import gui
from gui.qt import *
from gui.utils import showCritical

from googletrans import Translator
from googletrans.constants import LANGCODES


def on_translate(mw):
    gui.dialogs.open("TranslateDialog", mw)


class TranslateThread(QThread):

    prog = pyqtSignal(str)
    transed = pyqtSignal(int, dict)

    def __init__(self, mw, group, destcode, is_only):
        QThread.__init__(self)
        self.mw = mw
        self.group = group
        # Destination language to translate into
        self.translate = lambda text: Translator().translate(text, dest=destcode).text

        if is_only:
            self.targets = self.mw.entrylist.get_entry_selected()
        else:
            self.targets = self.mw.entrylist.get_entry_all()

    def run(self):
        assert self.targets

        for ew in self.targets:
            items = {}
            self.prog.emit(ew.editors['atop'].text())
            if 'atop' in self.group:
                items['atop'] = self.translate(ew.editors['atop'].text())

            for i in range(1, ew.lv1 + 1):
                _key = 'def-%d' % i
                define = ew.editors[_key].text()
                if _key in self.group and define != '':
                    items['def-%d' % i] = self.translate(define)

                for j in range(1, ew.lv2 + 1):
                    _key = 'ex-%d-%d' % (i, j)
                    examp = ew.editors[_key].text()
                    if _key in self.group and examp != '':
                        items['ex-%d-%d' % (i, j)] = self.translate(examp)

            self.transed.emit(ew.row, items)

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
        self.form.startButton.clicked.connect(self._translate)

        _list = self.form.keyList
        # Add checkbox corresponding to each _key of Entry
        for _key in self.mw.entrylist.setting._keys():
            check = QCheckBox(_key)
            lwi = QListWidgetItem()
            lwi.setSizeHint(check.sizeHint())
            _list.addItem(lwi)
            _list.setItemWidget(lwi, check)


    # Start translation
    def _translate(self):
        if self.mw.entrylist.count() == 0:
            showCritical("No entries found in your entry list.", title="Error")
            return

        form = self.form
        _keys = []
        # Get language code of target language to translate to from the library
        destcode = LANGCODES[form.langCombo.currentText().lower()]
        # Check which section to translate
        _list = form.keyList
        for i in range(_list.count()):
            ch = _list.itemWidget(_list.item(i))
            if ch.isChecked():
                _keys.append(ch.text())


        def _on_progress(name):
            self.form.pgMsg.setText("Translating %s." % name)
            val = self.form.progressBar.value()
            self.form.progressBar.setValue(val+1)

        # This causes a warning from PyQt about seting a parent on other thread.
        is_only = self.form.onlyCheck.isChecked()
        self.tt = TranslateThread(self.mw, _keys, destcode, is_only)
        self.form.progressBar.setRange(0, len(self.tt.targets))
        self.tt.prog.connect(_on_progress)
        self.tt.transed.connect(self.mw.entrylist.update_entry)
        self.tt.start()
        self.tt.finished.connect(lambda: self.reject(update=True))

    def reject(self, update=False):
        if update:
            self.mw.entrylist.update_all()
        self.done(0)
        gui.dialogs.close("TranslateDialog")
