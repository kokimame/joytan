from gui.qt import *
import gui
from tools.parser import Parsers
from tools.speecher import Speechers

class Preferences(QDialog):

    def __init__(self, mw, tab="General"):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.form = gui.forms.preferences.Ui_Preferences()
        self.form.setupUi(self)
        self.initUi()
        self.setTab(tab)
        self.show()

    def initUi(self):
        self.setupButtons()
        self.setupSpins()
        self.setupEditors()
        self.setupCombo()

    def setTab(self, tab):
        if tab == "General":
            self.form.tabWidget.setCurrentIndex(0)
        elif tab == "TTS":
            self.form.tabWidget.setCurrentIndex(1)


    def setupCombo(self):
        self.form.sourceCombo.addItems(sorted([site for site in Parsers.keys()]))
        self.form.sourceCombo.setCurrentText(self.mw.pref['onlineSrc'])
        self.form.ttsCombo.addItems(sorted([site for site in Speechers.keys()]))
        self.form.ttsCombo.setCurrentText(self.mw.pref['tts'])

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
        mw.pref['onlineSrc'] = form.sourceCombo.currentText()
        mw.pref['tts'] = form.ttsCombo.currentText()


    def reject(self):
        self.done(0)
        gui.dialogs.close("Preferences")
