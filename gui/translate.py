import gui
from gui.qt import *
from gui.utils import showCritical

from googletrans import Translator
from googletrans.constants import LANGCODES

def onTranslate(mw):
    gui.dialogs.open("TranslateDialog", mw)


class TranslateThread(QThread):

    sig = pyqtSignal(str)

    def __init__(self, mw, group, destCode):
        QThread.__init__(self)
        self.mw = mw
        self.group = group
        self.destCode = destCode

    def run(self):
        # FIXME: !!!!!!!!!!!WARNING!!!!!!!!!!!!
        # On Linux(Ubuntu), after translating English to other languages,
        # turning on the 'Edit' mode causes Segmentation fault and
        # the app ends with exit code 139.
        # As a note, this bug didn't occur before TranslateThread was introduced,
        # and cannot be reproduced on Mac and Windows
        translate = lambda text: Translator().translate(text, dest=self.destCode).text
        for ew in self.mw.entrylist.getEntries():
            self.sig.emit(ew.editors['atop'].text())
            if 'atop' in self.group:
                ew.editors['atop'].setText(translate(ew.editors['atop'].text()))
                self.mw.entrylist.setting.langMap['atop'][0] = self.destCode

            for i in range(1, ew.lv1 + 1):
                define = ew.editors['def-%d' % i].text()
                if 'definition' in self.group and define != '':
                    ew.editors['def-%d' % i].setText(translate(define))
                    self.mw.entrylist.setting.langMap['def-%d' % i][0] = self.destCode

                for j in range(1, ew.lv2 + 1):
                    examp = ew.editors['ex-%d-%d' % (i, j)].text()
                    if 'example' in self.group and examp != '':
                        ew.editors['ex-%d-%d' % (i, j)].setText(translate(examp))
                        self.mw.entrylist.setting.langMap['ex-%d-%d' % (i, j)][0] = self.destCode

        self.quit()


class TranslateDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.form = gui.forms.translate.Ui_TranslateDialog()
        self.form.setupUi(self)
        self.setupWidgets()
        self.show()

    def setupWidgets(self):
        form = self.form
        # Setup combo box for languages
        form.langCombo.addItems(sorted([lang.title() for lang in LANGCODES.keys()]))
        form.langCombo.setCurrentText("Japanese")
        form.startButton.clicked.connect(self.start)

    # Start translation
    def start(self):
        if self.mw.entrylist.count() == 0:
            showCritical("No entries found in your entry list.", title="Error")
            return

        form = self.form
        transGroup = []
        # Get language code of target language to translate to from the library
        destCode = LANGCODES[form.langCombo.currentText().lower()]
        if form.nameCheck.isChecked(): transGroup.append('atop')
        if form.defCheck.isChecked(): transGroup.append('definition')
        if form.exCheck.isChecked(): transGroup.append('example')

        print(transGroup)

        # This causes a warning from PyQt about seting a parent on other thread.
        self.tt = TranslateThread(self.mw, transGroup, destCode)
        self.form.progressBar.setRange(0, self.mw.entrylist.count())

        def onUpdate(name):
            self.form.pgMsg.setText("Translating %s." % name)
            val = self.form.progressBar.value()
            self.form.progressBar.setValue(val+1)

        self.tt.sig.connect(onUpdate)
        self.tt.start()
        self.tt.finished.connect(lambda: self.reject(update=True))

    def reject(self, update=False):
        if update:
            self.mw.entrylist.updateAll()
        self.done(0)
        gui.dialogs.close("TranslateDialog")
