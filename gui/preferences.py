from gui.qt import *
import gui
from tools.parser import Parsers
from tools.speecher import Speechers
from gui.utils import LANGUAGES, LANGCODES

class VlMapWidget(QWidget):
    # Maps between Voice and Language and play sample text-to-speech
    def __init__(self, tts, label, langCode):
        super(VlMapWidget, self).__init__()
        self.tts = Speechers[tts]
        self.label = label
        self.langCode = langCode
        self.initUi()

    def initUi(self):
        lbl = QLabel('%s:' % self.label.title())
        self.langCombo = QComboBox()
        self.langCombo.addItems(sorted([lang.title() for lang in LANGUAGES.values()]))
        self.langCombo.setCurrentText(LANGUAGES[self.langCode].title())
        self.langCombo.currentTextChanged.connect(self.updateVoiceCombo)
        lbl2 = QLabel('---> TTS:')
        self.voiceCombo = QComboBox()
        self.voiceCombo.addItems([name for name in self.tts.code2Names[self.langCode]])
        self.testBtn = QPushButton('Test')
        self.testBtn.clicked.connect(self.testVoice)

        hbox = QHBoxLayout()
        hbox.addWidget(lbl)
        hbox.addWidget(self.langCombo)
        hbox.addWidget(lbl2)
        hbox.addWidget(self.voiceCombo)
        hbox.addWidget(self.testBtn)
        self.setLayout(hbox)

    def updateVoiceCombo(self):
        self.langCode = LANGCODES[self.langCombo.currentText().lower()]
        self.voiceCombo.clear()
        self.voiceCombo.addItems([name for name in self.tts.code2Names[self.langCode]])
        self.voiceCombo.repaint()

    def testVoice(self):
        self.tts().preview(self.tts.code2Names[self.langCode][self.voiceCombo.currentText()])


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
        self.setupSpins()
        self.setupEditors()
        self.setupCombo()
        self.setupButtons()
        self.setupList()

    def setTab(self, tab):
        # Set by the absolute index of a tab based
        if tab == "General":
            self.form.tabWidget.setCurrentIndex(0)
        elif tab == "TTS":
            self.form.tabWidget.setCurrentIndex(1)

    def setupCombo(self):
        sc = self.form.sourceCombo
        tc = self.form.ttsCombo
        sc.addItems(sorted([site for site in Parsers.keys()]))
        sc.setCurrentText(self.mw.pref['onlineSrc'])
        tc.addItems(sorted([site for site in Speechers.keys()]))
        tc.setCurrentText(self.mw.pref['tts'])

    def setupButtons(self):
        form = self.form
        form.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.onOk)


    def setupList(self):
        testList = self.form.testList
        # Sort items in the order of 'name', 'def-x' and 'ex-x-x'
        for row in sorted(sorted(list(self.mw.framelist.setting.langMap.keys())),
                          key=lambda x: ['n', 'd', 'e'].index(x[0])):
            langCode = self.mw.framelist.setting.langMap[row]
            if langCode:
                wig = VlMapWidget(self.mw.pref['tts'], row, langCode)
            else:
                # Temporally we consider English as default
                wig = VlMapWidget(self.mw.pref['tts'], row, 'en')

            lwi = QListWidgetItem()
            lwi.setSizeHint(wig.sizeHint())
            testList.addItem(lwi)
            testList.setItemWidget(lwi, wig)

    def setupSpins(self):
        form = self.form
        fs = self.mw.framelist.setting
        form.dpwSpin.setValue(fs.dpw)
        form.epdSpin.setValue(fs.epd)

    def setupEditors(self):
        form = self.form
        mw = self.mw
        form.titleEdit.setText(mw.pref['title'])
        form.workingEdit.setText(mw.pref['workspace'])
        form.wordEdit.setText(mw.pref['worddir'])
        form.bgmEdit.setText(mw.pref['bgmdir'])
        form.sfxEdit.setText(mw.pref['sfxdir'])


    def onOk(self):
        self.updateBundlePref()
        self.updateMainPref()
        self.reject()


    def updateBundlePref(self):
        form = self.form
        fs = self.mw.framelist.setting
        fs.expand(dpw=form.dpwSpin.value())
        fs.expand(epd=form.epdSpin.value())

    def updateMainPref(self):
        form = self.form
        mw = self.mw
        mw.pref['title'] = form.titleEdit.text()
        mw.pref['workspace'] = form.workingEdit.text()
        mw.pref['worddir'] = form.wordEdit.text()
        mw.pref['bgmdir'] = form.bgmEdit.text()
        mw.pref['sfxdir'] = form.sfxEdit.text()
        mw.pref['onlineSrc'] = form.sourceCombo.currentText()
        mw.pref['tts'] = form.ttsCombo.currentText()


    def reject(self):
        self.done(0)
        gui.dialogs.close("Preferences")
