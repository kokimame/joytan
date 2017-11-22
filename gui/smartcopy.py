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
        if self.mw.framelist.count() == 0:
            showCritical("No bundles found.", title="Error")
            return

        form = self.form
        fbox, tbox = form.fromBox, form.toBox
        if fbox.currentText() == tbox.currentText():
            print("Choose different contents for copying")
            return

        # Copying from and to the contents in Bundle Widget
        for bw in self.mw.framelist.getCurrentBundleWidgets():
            try:
                bw.editors[tbox.currentText().lower()].setText(bw.editors[fbox.currentText().lower()].text())
            except KeyError:
                pass

        # Change language mapping of the framelist based on the copy
        fset = self.mw.framelist.setting
        fset.langMap[tbox.currentText().lower()][0] = fset.langMap[fbox.currentText().lower()][0]


        self.mw.framelist._update()

    def setupCombo(self):
        form = self.form
        fset = self.mw.framelist.setting
        form.fromBox.addItems([item.title() for item in fset.langMap])
        form.toBox.addItems([item.title() for item in fset.langMap])
        form.fromBox.setCurrentText('Name')

    def setupButtons(self):
        form = self.form
        form.copyBtn.clicked.connect(self.start)
        form.cancelBtn.clicked.connect(self.reject)

    def reject(self):
        self.done(0)
        gui.dialogs.close("CopyDialog")