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
        frame = self.mw.framelist

        # Sort items in the order of 'name', 'def-x' and 'ex-x-x'
        for row in sorted(sorted(list(frame.maxBundle.langMap.keys())),
                          key=lambda x: ['n', 'd', 'e'].index(x[0])):
            hbox = QHBoxLayout()
            lbl = QLabel('%s' % row.title())
            langCombo = QComboBox()
            langCombo.addItems(sorted([lang.title() for lang in LANGUAGES.values()]))
            lang = frame.maxBundle.langMap[row]
            if lang:
                langCombo.setCurrentText(LANGUAGES[lang].title())
            else:
                langCombo.setCurrentText(LANGUAGES['en'].title())
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
        gui.dialogs.close("LangDetectDialog")
