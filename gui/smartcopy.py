import gui
from gui.qt import *
from gui.utils import showCritical


def onCopy(mw):
    gui.dialogs.open("CopyDialog", mw)

class CopyDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.form = gui.forms.copydialog.Ui_CopyDialog()
        self.form.setupUi(self)
        self.setupCombo()
        self.setupButtons()
        self.show()

    def start(self):
        if self.mw.entrylist.count() == 0:
            showCritical("No entries found.", title="Error")
            return

        form = self.form
        fbox, tbox = form.fromBox, form.toBox
        if fbox.currentText() == tbox.currentText():
            print("Choose different contents for copying")
            return

        # Copying from and to the contents in Entry Widget
        for ew in self.mw.entrylist.getCurrentEntries():
            try:
                ew.editors[tbox.currentText().lower()].setText(ew.editors[fbox.currentText().lower()].text())
            except KeyError:
                pass

        # Change language mapping of the entrylist based on the copy
        eset = self.mw.entrylist.setting
        eset.langMap[tbox.currentText().lower()][0] = eset.langMap[fbox.currentText().lower()][0]


        self.mw.entrylist.updateAll()

    def setupCombo(self):
        form = self.form
        eset = self.mw.entrylist.setting
        form.fromBox.addItems([item.title() for item in eset.langMap])
        form.toBox.addItems([item.title() for item in eset.langMap])
        form.fromBox.setCurrentText('Name')

    def setupButtons(self):
        form = self.form
        form.copyBtn.clicked.connect(self.start)
        form.cancelBtn.clicked.connect(self.reject)

    def reject(self):
        self.done(0)
        gui.dialogs.close("CopyDialog")