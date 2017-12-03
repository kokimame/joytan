from gui.qt import *
import gui
from tools.parser import Parsers
from tools.speaker import Speaker
from gui.utils import LANGUAGES, LANGCODES
from gui.customs.lvmap import LvMapWidget


class Preferences(QDialog):

    def __init__(self, mw, tab="General"):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.eset = mw.entrylist.setting
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
        # Sort items in the order of 'atop', 'def-x' and 'ex-x-x'
        for key in sorted(list(self.eset.langMap.keys())):
            # language and Voice ID
            lv = self.eset.langMap[key]
            tag = self.eset.tags[key]

            wig = LvMapWidget(self.mw.pref['tts'], lv, tag)

            lwi = QListWidgetItem()
            lwi.setSizeHint(wig.sizeHint())
            testList.addItem(lwi)
            testList.setItemWidget(lwi, wig)

    def setupSpins(self):
        form = self.form
        form.dpwSpin.setValue(self.eset.dpw)
        form.epdSpin.setValue(self.eset.epd)

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
        for i in range(testList.count()):
            wig = testList.itemWidget(testList.item(i))
            # Key for Entry's dictionary of QLineEdit
            lineKey = self.eset.getKeyByTag(wig.tag)
            if lineKey in list(self.eset.langMap.keys()):
                newLang = LANGCODES[wig.langCombo.currentText().lower()]
                newVid = wig.tts.code2Vids[newLang][wig.voiceCombo.currentText()]
                self.eset.langMap[lineKey][0] = newLang
                self.eset.langMap[lineKey][1] = newVid

        self.eset.expand(dpw=self.form.dpwSpin.value())
        self.eset.expand(epd=self.form.epdSpin.value())



    def updateMainPref(self):
        form = self.form
        self.mw.pref['title'] = form.titleEdit.text()
        self.mw.pref['workspace'] = form.workingEdit.text()
        self.mw.pref['worddir'] = form.wordEdit.text()
        self.mw.pref['bgmdir'] = form.bgmEdit.text()
        self.mw.pref['sfxdir'] = form.sfxEdit.text()
        self.mw.pref['onlineSrc'] = form.sourceCombo.currentText()
        self.mw.pref['tts'] = form.ttsCombo.currentText()


    def reject(self):
        self.done(0)
        gui.dialogs.close("Preferences")
