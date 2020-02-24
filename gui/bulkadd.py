
import gui
from gui.qt import *
from gui.utils import showCritical, showWarning


def on_bulkadd(ad):
    gui.dialogs.open("BulkaddDialog", ad)


class BulkaddDialog(QDialog):
    def __init__(self, ad):
        QDialog.__init__(self, ad, Qt.Window)
        self.ad = ad
        self._ui()
        self.show()

    def _ui(self):
        self.form = gui.forms.bulkadd.Ui_BulkaddDialog()
        self.form.setupUi(self)
        self.form.buttonBox.accepted.connect(self._on_ok)

    def _on_ok(self):
        text=self.form.lineEdit.text()
        self.ad.bulkadd_flow(text)


    def reject(self):
        self.done(0)
        gui.dialogs.close("BulkaddDialog")
