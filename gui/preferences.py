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
        self.setupEditors()

    def setupButtons(self):
        form = self.form
        form.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.onOk)

    def setupSpins(self):
        form = self.form
        factory = self.mw.bdfactory
        form.dpwSpin.setValue(factory.pref['dpw'])
        form.epdSpin.setValue(factory.pref['epd'])

    def setupEditors(self):
        form = self.form
        fm = self.mw.fm
        form.titleEdit.setText(fm.pref['title'])
        form.workingEdit.setText(fm.pref['workdir'])
        form.wordEdit.setText(fm.pref['worddir'])
        form.bgmEdit.setText(fm.pref['bgmdir'])
        form.sfxEdit.setText(fm.pref['sfxdir'])


    def onOk(self):
        self.updateBundlePref()
        self.updateFramePref()
        self.reject()

    def updateBundlePref(self):
        form = self.form
        factory = self.mw.bdfactory
        factory.pref['dpw'] = form.dpwSpin.value()
        factory.pref['epd'] = form.epdSpin.value()

    def updateFramePref(self):
        form = self.form
        fm = self.mw.fm
        fm.pref['title'] = form.titleEdit.text()
        fm.pref['workdir'] = form.workingEdit.text()
        fm.pref['worddir'] = form.wordEdit.text()
        fm.pref['bgmdir'] = form.bgmEdit.text()
        fm.pref['sfxdir'] = form.sfxEdit.text()


    def reject(self):
        self.done(0)
        gui.dialogs.close("Preferences")