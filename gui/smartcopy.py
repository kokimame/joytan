from gui.qt import *
import gui

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
        pass

    def setupCombo(self):
        form = self.form
        fset = self.mw.framelist.setting
        form.fromBox.addItems([item.title() for item in fset.langMap])
        form.toBox.addItems([item.title() for item in fset.langMap])
        form.fromBox.setCurrentText('Name')

    def setupButtons(self):
        form = self.form
        form.okBtn.clicked.connect(self.start)
        form.cancelBtn.clicked.connect(self.reject)

    def reject(self):
        self.done(0)
        gui.dialogs.close("CopyDialog")