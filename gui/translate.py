from gui.qt import *
import gui

from googletrans import Translator
from googletrans.constants import LANGCODES


def onTranslate(mw):
    gui.dialogs.open("TranslateDialog", mw)


class TranslateDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.framelist = mw.framelist
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
        translate = lambda text: Translator().translate(text, dest=destCode).text

        for bw in self.framelist.getCurrentBundleWidgets():
            if 'name' in transGroup:
                bw.editors['name'].setText(translate(bw.name))

            for i in range(1, bw.dpw+1):
                define = bw.editors['def-%d' % i].text()
                if 'definition' in transGroup and define != '':
                    bw.editors['def-%d' % i].setText(translate(define))

                for j in range(1, bw.epd+1):
                    examp = bw.editors['ex-%d-%d' % (i, j)].text()
                    if 'example' in transGroup and examp != '':
                        bw.editors['ex-%d-%d' % (i, j)].setText(translate(examp))
        
        self.framelist._update()
        self.reject()





    def reject(self):
        self.done(0)
        gui.dialogs.close("TranslateDialog")
