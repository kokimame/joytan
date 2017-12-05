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
        sc.setCurrentText(self.mw.setting['onlineSrc'])
        tc.addItems(sorted([site for site in Speaker.keys()]))
        tc.setCurrentText(self.mw.setting['tts'])

    def setupButtons(self):
        form = self.form
        form.okBtn.clicked.connect(self.onOk)
        form.applyBtn.clicked.connect(self.onApply)


    def setupList(self):
        testList = self.form.testList
        tagList = self.form.tagList
        # Sort keys for Entry's dict of QLineEdit alphabetically
        # i.e. 'atop', 'def-x' and 'ex-x-x'
        for lineKey in sorted(list(self.eset.langMap.keys())):
            # language and Voice ID
            lv = self.eset.langMap[lineKey]
            tag = self.eset.tags[lineKey]

            wig = LvMapWidget(self.mw.setting['tts'], lv, tag)

            lwi1 = QListWidgetItem()
            lwi1.setSizeHint(wig.sizeHint())
            testList.addItem(lwi1)
            testList.setItemWidget(lwi1, wig)

            lwi2 = QListWidgetItem()
            tagEdit = QLineEdit(self.eset.tags[lineKey])
            tagList.addItem(lwi2)
            tagList.setItemWidget(lwi2, tagEdit)

    def setupSpins(self):
        form = self.form
        form.dpwSpin.setValue(self.eset.dpw)
        form.epdSpin.setValue(self.eset.epd)

    def setupEditors(self):
        form = self.form
        mw = self.mw
        form.titleEdit.setText(mw.setting['title'])
        form.workingEdit.setText(mw.setting['workspace'])
        form.wordEdit.setText(mw.setting['worddir'])
        form.bgmEdit.setText(mw.setting['bgmdir'])
        form.sfxEdit.setText(mw.setting['sfxdir'])


    def onOk(self):
        # FIXME: Switching TTS service may break LvMapping.
        self.updateEntrySetting()
        self.updateMainSetting()
        self.reject()

    def onApply(self):
        self.updateEntrySetting()
        self.updateMainSetting()
        self.form.testList.clear()
        self.form.tagList.clear()

        self.initUi()

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



    def updateMainSetting(self):
        form = self.form
        self.mw.setting['title'] = form.titleEdit.text()
        self.mw.setting['workspace'] = form.workingEdit.text()
        self.mw.setting['worddir'] = form.wordEdit.text()
        self.mw.setting['bgmdir'] = form.bgmEdit.text()
        self.mw.setting['sfxdir'] = form.sfxEdit.text()
        self.mw.setting['onlineSrc'] = form.sourceCombo.currentText()
        self.mw.setting['tts'] = form.ttsCombo.currentText()


    def reject(self):
        self.done(0)
        gui.dialogs.close("Preferences")
