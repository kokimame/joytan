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

    def __init__(self, mw, group, destcode):
        QThread.__init__(self)
        self.mw = mw
        self.group = group
        # Destination language to translate into
        self.translate = lambda text: Translator().translate(text, dest=destcode).text

    def run(self):
        for ew in self.mw.entrylist.get_entry_all():
            items = {}
            self.prog.emit(ew.editors['atop'].text())
            if 'atop' in self.group:
                items['atop'] = self.translate(ew.editors['atop'].text())

            for i in range(1, ew.lv1 + 1):
                define = ew.editors['def-%d' % i].text()
                if 'definition' in self.group and define != '':
                    items['def-%d' % i] = self.translate(define)

                for j in range(1, ew.lv2 + 1):
                    examp = ew.editors['ex-%d-%d' % (i, j)].text()
                    if 'example' in self.group and examp != '':
                        items['ex-%d-%d' % (i, j)] = self.translate(examp)

            self.transed.emit(ew.row, items)

        self.quit()


class TranslateDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.form = gui.forms.translate.Ui_TranslateDialog()
        self.form.setupUi(self)
        self._ui()
        self.show()

    def _ui(self):
        form = self.form
        # Setup combo box for languages
        form.langCombo.addItems(sorted([lang.title() for lang in LANGCODES.keys()]))
        form.langCombo.setCurrentText("Japanese")
        form.startButton.clicked.connect(self._translate)

    # Start translation
    def _translate(self):
        if self.mw.entrylist.count() == 0:
            showCritical("No entries found in your entry list.", title="Error")
            return

        form = self.form
        group = []
        # Get language code of target language to translate to from the library
        destcode = LANGCODES[form.langCombo.currentText().lower()]
        # Check which section to translate
        if form.nameCheck.isChecked():
            group.append('atop')
        if form.defCheck.isChecked():
            group.append('definition')
        if form.exCheck.isChecked():
            group.append('example')

        def _on_progress(name):
            self.form.pgMsg.setText("Translating %s." % name)
            val = self.form.progressBar.value()
            self.form.progressBar.setValue(val+1)

        # This causes a warning from PyQt about seting a parent on other thread.
        self.tt = TranslateThread(self.mw, group, destcode)
        self.form.progressBar.setRange(0, self.mw.entrylist.count())
        self.tt.prog.connect(_on_progress)
        self.tt.transed.connect(self.mw.entrylist.update_entry)
        self.tt.start()
        self.tt.finished.connect(lambda: self.reject(update=True))

    def reject(self, update=False):
        if update:
            self.mw.entrylist.update_all()
        self.done(0)
        gui.dialogs.close("TranslateDialog")
