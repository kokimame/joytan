from gui.qt import *
import gui
from tools.parser import Parsers
from tools.speaker import Speaker
from gui.utils import LANGUAGES, LANGCODES
from gui.customs import LvMapWidget


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
        tc.addItems(sorted([site for site in Speaker.keys()]))
        tc.setCurrentText(self.mw.pref['tts'])

    def setupButtons(self):
        form = self.form
        form.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.onOk)


    def setupList(self):
        testList = self.form.testList
        testList.setStyleSheet("""
                            QListWidget::item { border-bottom: 1px solid black; }
                           """)
        # Sort items in the order of 'name', 'def-x' and 'ex-x-x'
        for item in sorted(sorted(list(self.mw.entrylist.setting.langMap.keys())),
                          key=lambda x: ['n', 'd', 'e'].index(x[0])):
            # language and Voice ID
            lv = self.mw.entrylist.setting.langMap[item]

            wig = LvMapWidget(self.mw.pref['tts'], item, lv)

            lwi = QListWidgetItem()
            lwi.setSizeHint(wig.sizeHint())
            testList.addItem(lwi)
            testList.setItemWidget(lwi, wig)

    def setupSpins(self):
        form = self.form
        fs = self.mw.entrylist.setting
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
        self.updateEntrySetting()
        self.updateMainPref()
        self.reject()

    def updateEntrySetting(self):
        testList = self.form.testList
        eset = self.mw.entrylist.setting
        for i in range(testList.count()):
            wig = testList.itemWidget(testList.item(i))
            if wig.label in eset.langMap:
                newLang = LANGCODES[wig.langCombo.currentText().lower()]
                newVid = wig.tts.code2Vids[newLang][wig.voiceCombo.currentText()]
                eset.langMap[wig.label][0] = newLang
                eset.langMap[wig.label][1] = newVid

        eset.expand(dpw=self.form.dpwSpin.value())
        eset.expand(epd=self.form.epdSpin.value())



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
