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
        # then turning on the 'Edit' mode causes Segmentation fault then
        # the app ends with exit code 139.
        # As a note, this bug didn't occur before TranslateThread was introduced,
        # and also this bug does not occur at least on Mac.
        translate = lambda text: Translator().translate(text, dest=self.destCode).text
        for bw in self.mw.framelist.getCurrentBundleWidgets():
            self.sig.emit(bw.name)
            if 'name' in self.group:
                bw.editors['name'].setText(translate(bw.name))
                self.mw.framelist.setting.langMap['name'][0] = self.destCode

            for i in range(1, bw.dpw + 1):
                define = bw.editors['def-%d' % i].text()
                if 'definition' in self.group and define != '':
                    bw.editors['def-%d' % i].setText(translate(define))
                    self.mw.framelist.setting.langMap['def-%d' % i][0] = self.destCode

                for j in range(1, bw.epd + 1):
                    examp = bw.editors['ex-%d-%d' % (i, j)].text()
                    if 'example' in self.group and examp != '':
                        bw.editors['ex-%d-%d' % (i, j)].setText(translate(examp))
                        self.mw.framelist.setting.langMap['ex-%d-%d' % (i, j)][0] = self.destCode

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
        if self.mw.framelist.count() == 0:
            showCritical("No bundles found.", title="Error")
            return

        form = self.form
        transGroup = []
        # Get language code of target language to translate to from the library
        destCode = LANGCODES[form.langCombo.currentText().lower()]
        if form.nameCheck.isChecked(): transGroup.append('name')
        if form.defCheck.isChecked(): transGroup.append('definition')
        if form.exCheck.isChecked(): transGroup.append('example')

        print(transGroup)

        # This causes a warning from PyQt about seting a parent on other thread.
        self.tt = TranslateThread(self.mw, transGroup, destCode)
        self.form.progressBar.setRange(0, self.mw.framelist.count())

        def onUpdate(name):
            self.form.pgMsg.setText("Translating %s." % name)
            val = self.form.progressBar.value()
            self.form.progressBar.setValue(val+1)

        self.tt.sig.connect(onUpdate)
        self.tt.start()
        self.tt.finished.connect(lambda: self.reject(update=True))

    def reject(self, update=False):
        if update:
            self.mw.framelist._update()
        self.done(0)
        gui.dialogs.close("TranslateDialog")
