from gui.qt import *
import gui
from tools.parser import Parsers
from tools.speecher import Speechers
from gui.utils import LANGUAGES, LANGCODES

class LvMapWidget(QWidget):
    # Maps from content type and language code and Voice ID, and test sample text-to-speech
    def __init__(self, tts, label, lv):
        super(LvMapWidget, self).__init__()
        self.tts = Speechers[tts]
        self.label = label
        # Language and Voice ID for the label (e.g, 'name' or 'def-x' etc)
        self.lv = lv
        self.initUi()

    def initUi(self):
        lbl = QLabel('%s:' % self.label.title())
        self.langCombo = QComboBox()
        self.langCombo.addItems(sorted([lang.title() for lang in LANGUAGES.values()]))
        self.langCombo.setCurrentText(LANGUAGES[self.lv[0]].title())
        self.langCombo.currentTextChanged.connect(self.updateVoiceCombo)
        lbl2 = QLabel('---> TTS:')
        self.voiceCombo = QComboBox()
        self.voiceCombo.addItems([name for name in self.tts.code2Vids[self.lv[0]]])
        if self.lv[1]:
            self.voiceCombo.setCurrentText(self.lv[1])
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
        self.lv[0] = LANGCODES[self.langCombo.currentText().lower()]
        self.voiceCombo.clear()
        self.voiceCombo.addItems([name for name in self.tts.code2Vids[self.lv[0]]])
        self.voiceCombo.repaint()

    def testVoice(self):
        self.tts().preview(self.tts.code2Vids[self.lv[0]][self.voiceCombo.currentText()])


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
            # language and Voice ID
            lv = self.mw.framelist.setting.langMap[row]

            wig = LvMapWidget(self.mw.pref['tts'], row, lv)

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
        # FIXME: Switching TTS service may break LvMapping.
        self.updateFrameSetting()
        self.updateMainPref()
        self.reject()

    def updateFrameSetting(self):
        testList = self.form.testList
        fset = self.mw.framelist.setting
        for i in range(testList.count()):
            wig = testList.itemWidget(testList.item(i))
            if wig.label in fset.langMap:
                fset.langMap[wig.label][0] = LANGCODES[wig.langCombo.currentText().lower()]
                fset.langMap[wig.label][1] = wig.voiceCombo.currentText()

        fs = self.mw.framelist.setting
        fs.expand(dpw=self.form.dpwSpin.value())
        fs.expand(epd=self.form.epdSpin.value())



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
