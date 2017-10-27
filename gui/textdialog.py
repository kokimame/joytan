from gui.qt import *
import gui

def onTextDialog(mw):
    gui.dialogs.open("TextDialog", mw)

class TextDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.framelist = self.mw.framelist

        self.form = gui.forms.textdialog.Ui_TextDialog()
        self.form.setupUi(self)
        self.show()