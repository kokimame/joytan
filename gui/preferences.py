from gui.qt import *
import gui

class Preferences(QDialog):

    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.form = gui.forms.preferences.Ui_preferences()
        self.form.setupUi(self)
        self.form.buttonBox.button(QDialogButtonBox.Help).setAutoDefault(False)
        self.form.buttonBox.button(QDialogButtonBox.Close).setAutoDefault(False)
        self.show()

    def reject(self):
        self.done(0)
        gui.dialogs.close("Preferences")