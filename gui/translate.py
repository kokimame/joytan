from gui.qt import *
import gui

from googletrans import Translator
from googletrans.constants import LANGCODES

def onTranslate(mw):
    gui.dialogs.open("TranslateDialog", mw)


class TranslateDialog(QDialog):

    class TranslateThread(QThread):
        def __init__(self, mw, group, destCode):
            QThread.__init__(self)
            self.mw = mw
            self.group = group
            self.destCode = destCode

        def run(self):
            translate = lambda text: Translator().translate(text, dest=self.destCode).text
            self.mw.progress.start(min=0, max=self.mw.framelist.count(),
                                   label="Start translating", immediate=True, cancellable=True)
            for bw in self.mw.framelist.getCurrentBundleWidgets():
                self.mw.progress.update(label="Translating %s" % bw.name, maybeShow=False)
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

            self.mw.progress.finish()

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
        form = self.form
        transGroup = []
        # Get language code of target language to translate to from the library
        destCode = LANGCODES[form.langCombo.currentText().lower()]
        if form.nameCheck.isChecked(): transGroup.append('name')
        if form.defCheck.isChecked(): transGroup.append('definition')
        if form.exCheck.isChecked(): transGroup.append('example')

        print(transGroup)
        transThread = self.TranslateThread(self.mw, transGroup, destCode)
        transThread.run()

        self.mw.framelist._update()
        self.reject()

    def reject(self):
        self.done(0)
        gui.dialogs.close("TranslateDialog")
