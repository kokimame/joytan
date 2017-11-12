import gui
from gui.qt import *
from gui.utils import LANGUAGES

class LangDetectDialog(QDialog):
    def __init__(self, mw, itemLang):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.framelist = mw.framelist
        self.form = gui.forms.langdetect.Ui_LangDetectDialog()
        self.form.setupUi(self)
        self.setupList(itemLang)
        self.setupButtons()
        self.show()

    def setupList(self, itemLang):
        langlist = self.form.langList
        for row, lang in itemLang.items():
            hbox = QHBoxLayout()
            lbl = QLabel('%s' % row.title())
            langCombo = QComboBox()
            langCombo.addItems(sorted([lang.title() for lang in LANGUAGES.values()]))
            if lang:
                langCombo.setCurrentText(LANGUAGES[lang].title())
            hbox.addWidget(lbl)
            hbox.addWidget(langCombo)
            wig = QWidget()
            wig.setLayout(hbox)
            lwi = QListWidgetItem()
            lwi.setSizeHint(wig.sizeHint())
            langlist.addItem(lwi)
            langlist.setItemWidget(lwi, wig)

    def setupButtons(self):
        form = self.form
        form.cancelBtn.clicked.connect(self.reject)
        form.okBtn.clicked.connect(self.reject)

    def reject(self):
        self.done(0)
        gui.dialogs.close("TranslateDialog")
