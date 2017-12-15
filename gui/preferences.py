import gui
from gui.widgets.lvmap import LvMapWidget
from gui.qt import *
from gui.utils import LANGCODES
from tools.speaker import Speaker


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
        self.setupATTS()

    def setupATTS(self):
        from gui.widgets.awesometts import AwesomeTTS
        from gui.utils import showCritical, getText
        tab = self.form.tabAtts
        hbox= QHBoxLayout()
        hbox.addWidget(AwesomeTTS(showCritical, getText))
        tab.setLayout(hbox)

    def setTab(self, tab):
        # Set by the absolute index of a tab based
        if tab == "General":
            self.form.tabWidget.setCurrentIndex(0)
        elif tab == "TTS":
            self.form.tabWidget.setCurrentIndex(1)

    def setupCombo(self):
        tc = self.form.ttsCombo
        tc.addItems(sorted([site for site in Speaker.keys()]))
        tc.setCurrentText(self.mw.setting['tts'])

    def setupButtons(self):
        form = self.form
        form.okBtn.clicked.connect(self.onOk)
        form.applyBtn.clicked.connect(self.onApply)


    def setupList(self):
        testList = self.form.testList
        # Sort keys for Entry's dict of QLineEdit alphabetically
        # i.e. 'atop', 'def-x' and 'ex-x-x'
        for lineKey in sorted(list(self.eset.langMap.keys())):
            # language and Voice ID
            lv = self.eset.langMap[lineKey]
            wig = LvMapWidget(self.mw.setting['tts'], lv, lineKey)

            lwi1 = QListWidgetItem()
            lwi1.setSizeHint(wig.sizeHint())
            testList.addItem(lwi1)
            testList.setItemWidget(lwi1, wig)

    def setupSpins(self):
        form = self.form
        form.dpwSpin.setValue(self.eset.lv1)
        form.epdSpin.setValue(self.eset.lv2)

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

        self.initUi()

    def updateEntrySetting(self):
        testList = self.form.testList
        for i in range(testList.count()):
            wig = testList.itemWidget(testList.item(i))
            # Key for Entry's dictionary of QLineEdit
            lineKey = wig.key
            if lineKey in list(self.eset.langMap.keys()):
                newLang = LANGCODES[wig.langCombo.currentText().lower()]
                newVid = wig.tts.code2Vids[newLang][wig.voiceCombo.currentText()]
                self.eset.langMap[lineKey][0] = newLang
                self.eset.langMap[lineKey][1] = newVid

        self.eset.reshape(lv1=self.form.dpwSpin.value())
        self.eset.reshape(lv2=self.form.epdSpin.value())



    def updateMainSetting(self):
        form = self.form
        self.mw.setting['title'] = form.titleEdit.text()
        self.mw.setting['workspace'] = form.workingEdit.text()
        self.mw.setting['worddir'] = form.wordEdit.text()
        self.mw.setting['bgmdir'] = form.bgmEdit.text()
        self.mw.setting['sfxdir'] = form.sfxEdit.text()
        self.mw.setting['tts'] = form.ttsCombo.currentText()


    def reject(self):
        self.done(0)
        gui.dialogs.close("Preferences")
