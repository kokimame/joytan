from gui.qt import *
import gui

class Preferences(QDialog):

    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.form = gui.forms.preferences.Ui_preferences()
        self.form.setupUi(self)
        self.initUi()
        self.show()

    def initUi(self):
        self.setupButtons()
        self.setupSpins()

    def setupButtons(self):
        form = self.form
        form.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.onOk)

    def setupSpins(self):
        form = self.form
        factory = self.mw.bdfactory
        form.dpwSpin.setValue(factory.pref['dpw'])
        form.epdSpin.setValue(factory.pref['epd'])


    def onOk(self):
        self.updateBundlePref()
        self.reject()

    def updateBundlePref(self):
        form = self.form
        factory = self.mw.bdfactory
        factory.pref['dpw'] = form.dpwSpin.value()
        factory.pref['epd'] = form.epdSpin.value()


    def reject(self):
        self.done(0)
        gui.dialogs.close("Preferences")