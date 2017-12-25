import gui
from gui.qt import *
from gui.utils import showCritical


def on_copy(mw):
    gui.dialogs.open("CopyDialog", mw)


class CopyDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self._ui()
        self.show()

    def _ui(self):
        self.form = gui.forms.copydialog.Ui_CopyDialog()
        self.form.setupUi(self)
        eset = self.mw.entrylist.setting

        self.form.fromBox.addItems([item for item in sorted(eset.ttsmap)])
        self.form.toBox.addItems([item for item in sorted(eset.ttsmap)])
        self.form.fromBox.setCurrentText('atop')
        self.form.copyBtn.clicked.connect(self._copy)
        self.form.cancelBtn.clicked.connect(self.reject)

    def _copy(self):
        if self.mw.entrylist.count() == 0:
            showCritical("No entries found in your entry list.", title="Error")
            return

        form = self.form
        fbox, tbox = form.fromBox, form.toBox
        if fbox.currentText() == tbox.currentText():
            print("Choose different contents for copying")
            return

        # Copying from and to the contents in Entry Widget
        for ew in self.mw.entrylist.get_entry_all():
            try:
                ew.editors[tbox.currentText()].setText(ew.editors[fbox.currentText()].text())
            except KeyError:
                pass

        # Change language mapping of the entrylist based on the copy
        eset = self.mw.entrylist.setting
        eset.ttsmap[tbox.currentText()] = eset.ttsmap[fbox.currentText()]

        self.mw.entrylist.update_all()

    def reject(self):
        self.done(0)
        gui.dialogs.close("CopyDialog")
