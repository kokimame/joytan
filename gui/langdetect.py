import gui
from gui.qt import *
from gui.utils import LANGUAGES, LANGCODES

class LangWidget(QWidget):
    def __init__(self, label, langCode):
        super(LangWidget, self).__init__()
        self.label = label
        self.langCode = langCode
        self.initUi()

    def initUi(self):
        lbl = QLabel('%s' % self.label.title())
        self.langCombo = QComboBox()
        self.langCombo.addItems(sorted([lang.title() for lang in LANGUAGES.values()]))
        self.langCombo.setCurrentText(LANGUAGES[self.langCode].title())

        hbox = QHBoxLayout()
        hbox.addWidget(lbl)
        hbox.addWidget(self.langCombo)
        self.setLayout(hbox)


class LangDetectDialog(QDialog):
    def __init__(self, mw, langMap=None):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.framelist = mw.framelist
        self.form = gui.forms.langdetect.Ui_LangDetectDialog()
        self.form.setupUi(self)
        self.setupList(langMap)
        self.setupButtons()
        self.show()

    def setupList(self, langMap):
        self.comboMap = {}
        langlist = self.form.langList
        framelist = self.mw.framelist
        if langMap:
            newKeys = list(langMap.keys())
        else:
            newKeys = []

        # Sort items in the order of 'name', 'def-x' and 'ex-x-x'
        for row in sorted(sorted(list(framelist.setting.langMap.keys())),
                          key=lambda x: ['n', 'd', 'e'].index(x[0])):

            if row in newKeys:
                wig = LangWidget(row, langMap[row])
            else:
                langCode = framelist.setting.langMap[row]
                if langCode:
                    wig = LangWidget(row, langCode)
                else:
                    # Temporally we consider English as default
                    wig = LangWidget(row, 'en')

            lwi = QListWidgetItem()
            lwi.setSizeHint(wig.sizeHint())
            langlist.addItem(lwi)
            langlist.setItemWidget(lwi, wig)

    def setupButtons(self):
        form = self.form
        form.cancelBtn.clicked.connect(self.reject)
        form.okBtn.clicked.connect(self.onOk)

    def onOk(self):
        langlist = self.form.langList
        framelist = self.mw.framelist
        for i in range(langlist.count()):
            wig = langlist.itemWidget(langlist.item(i))
            framelist.setting.langMap[wig.label] = LANGCODES[wig.langCombo.currentText().lower()]

        self.reject()

    def reject(self):
        self.done(0)
        gui.dialogs.close("LangDetectDialog")
