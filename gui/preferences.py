from gui.qt import *
import gui

class Preferences(QDialog):

    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.form = gui.forms.preferences.Ui_Preferences()
        self.form.setupUi(self)
        self.initUi()
        self.show()

    def initUi(self):
        self.setupButtons()
        self.setupSpins()
        self.setupEditors()
        self.setupCombo()

    def setupCombo(self):
        self.form.dictCombo.setCurrentText(self.mw.pref['onlineRef'])

    def setupButtons(self):
        form = self.form
        form.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.onOk)

    def setupSpins(self):
        form = self.form
        factory = self.mw.framelist.bf
        form.dpwSpin.setValue(factory.pref['dpw'])
        form.epdSpin.setValue(factory.pref['epd'])

    def setupEditors(self):
        form = self.form
        mw = self.mw
        form.titleEdit.setText(mw.pref['title'])
        form.workingEdit.setText(mw.pref['workdir'])
        form.wordEdit.setText(mw.pref['worddir'])
        form.bgmEdit.setText(mw.pref['bgmdir'])
        form.sfxEdit.setText(mw.pref['sfxdir'])


    def onOk(self):
        self.updateBundlePref()
        self.updateMainPref()
        self.reject()


    def updateBundlePref(self):
        form = self.form
        factory = self.mw.framelist.bf
        factory.pref['dpw'] = form.dpwSpin.value()
        factory.pref['epd'] = form.epdSpin.value()

    def updateMainPref(self):
        form = self.form
        mw = self.mw
        mw.pref['title'] = form.titleEdit.text()
        mw.pref['workdir'] = form.workingEdit.text()
        mw.pref['worddir'] = form.wordEdit.text()
        mw.pref['bgmdir'] = form.bgmEdit.text()
        mw.pref['sfxdir'] = form.sfxEdit.text()
        mw.pref['onlineRef'] = form.dictCombo.currentText()


    def reject(self):
        self.done(0)
        gui.dialogs.close("Preferences")
