import gui
from gui.qt import *
from gui.utils import LANGCODES
from gui.widgets.awesometts import AwesomeTTS


class Preferences(QDialog):
    _INDEX_GENERAL = 0
    _INDEX_ATTS = 2

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
        self.setupATTS()
        form = self.form
        # Buttons
        form.okBtn.clicked.connect(self.onOk)
        form.applyBtn.clicked.connect(self.onApply)
        # Spins
        form.dpwSpin.setValue(self.eset.lv1)
        form.epdSpin.setValue(self.eset.lv2)
        # Editors
        form.titleEdit.setText(self.mw.setting['title'])
        form.workingEdit.setText(self.mw.setting['workspace'])
        form.wordEdit.setText(self.mw.setting['worddir'])
        form.bgmEdit.setText(self.mw.setting['bgmdir'])
        form.sfxEdit.setText(self.mw.setting['sfxdir'])

    def setupATTS(self):
        tab = self.form.tabAtts
        if not tab.layout():
            from gui.utils import showCritical, getText
            atts = AwesomeTTS(self.eset, showCritical, getText)
            atts.setObjectName("AwesomeTTS")
            hbox = QHBoxLayout()
            hbox.addWidget(atts)
            tab.setLayout(hbox)

    def setTab(self, tab):
        # Set by the absolute index of a tab based
        if tab == "General":
            self.form.tabWidget.setCurrentIndex(0)
        elif tab == "TTS":
            self.form.tabWidget.setCurrentIndex(1)

    def onOk(self):
        # FIXME: Switching TTS service may break LvMapping.
        self.updateSetting()
        self.reject()

    def onApply(self):
        self.updateSetting()
        self.initUi()

    def updateSetting(self):
        form = self.form
        self.mw.setting['title'] = form.titleEdit.text()
        self.mw.setting['workspace'] = form.workingEdit.text()
        self.mw.setting['worddir'] = form.wordEdit.text()
        self.mw.setting['bgmdir'] = form.bgmEdit.text()
        self.mw.setting['sfxdir'] = form.sfxEdit.text()

        self.eset.reshape(lv1=self.form.dpwSpin.value())
        self.eset.reshape(lv2=self.form.epdSpin.value())


    def reject(self):
        self.done(0)
        gui.dialogs.close("Preferences")
