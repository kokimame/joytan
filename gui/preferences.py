import gui
from gui.qt import *
from gui.utils import LANGCODES
from gui.widgets.awesometts import AwesomeTTS


class Preferences(QDialog):
    _INDEX_GENERAL = 0
    _INDEX_ATTS = 2

    def __init__(self, mw, tab="General", back_to=None):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        # Specify the dialog that regains focus after closing Preference,
        # the MainWindow does so by default.
        # The variable only gets called on reject for activateWindow and raise_
        # FIXME: This may be done natively by configuring instanciation or modality of dialogs.
        # FIXME: How can it be tested that the right dialog regains focus after some event
        self.back_to = back_to or None
        self.form = gui.forms.preferences.Ui_Preferences()
        self.form.setupUi(self)
        self._ui()
        self._ui_atts()
        self._set_tab(tab)
        self.show()

    def _ui(self):
        form = self.form
        el = self.mw.entrylist
        # Buttons
        form.okBtn.clicked.connect(self.on_ok)
        form.applyBtn.clicked.connect(self.on_apply)
        # Spins
        form.dpwSpin.setValue(el.get_config('ndef'))
        form.epdSpin.setValue(el.get_config('nex'))
        # Editors
        form.titleEdit.setText(self.mw.config['title'])
        form.workingEdit.setText(self.mw.config['workspace'])
        form.wordEdit.setText(self.mw.config['worddir'])
        form.bgmEdit.setText(self.mw.config['bgmdir'])
        form.sfxEdit.setText(self.mw.config['sfxdir'])

    def _ui_atts(self):
        """
        Build AwesomeTTS integration 
        """
        tab = self.form.tabAtts
        if not tab.layout():
            from gui.utils import showCritical, getText
            el = self.mw.entrylist
            atts = AwesomeTTS((el.get_config, el.set_config), showCritical, getText)
            atts.setObjectName("AwesomeTTS")
            hbox = QHBoxLayout()
            hbox.addWidget(atts)
            tab.setLayout(hbox)

    def _set_tab(self, tab):
        # Set by the absolute index of a tab based
        if tab == "General":
            self.form.tabWidget.setCurrentIndex(0)
        elif tab == "TTS":
            self.form.tabWidget.setCurrentIndex(1)

    def on_ok(self):
        self._update()
        self.reject()

    def on_apply(self):
        self._update()
        self._ui()

    def _update(self):
        form = self.form
        self.mw.config['title'] = form.titleEdit.text()
        self.mw.config['workspace'] = form.workingEdit.text()
        self.mw.config['worddir'] = form.wordEdit.text()
        self.mw.config['bgmdir'] = form.bgmEdit.text()
        self.mw.config['sfxdir'] = form.sfxEdit.text()
        self.mw.entrylist.set_config('reshape',
                                     dict(ndef=self.form.dpwSpin.value(), nex=self.form.epdSpin.value()))

    def reject(self):
        if self.back_to:
            self.back_to.activateWindow()
            self.back_to.raise_()
        self.done(0)
        gui.dialogs.close("Preferences")
