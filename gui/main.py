import os
import json

import gui
from gui import ICONS
from gui.qt import *
from gui.utils import isMac, isLin, isWin


def default_setting():
    cwd = os.getcwd()
    setting = None

    with open(os.path.join(cwd, "mysetting.json"), 'r') as f:
        js_setting = json.loads(f.read())

    if isLin:
        setting = js_setting['linux']
    elif isMac:
        setting = js_setting['mac']
    elif isWin:
        setting = js_setting['windows']

    return {
        "workspace": os.path.join(*setting['workspace']),
        "title": js_setting['title'],
        "sfxdir": os.path.join(cwd, "templates", "sfx"),
        "worddir": os.path.join(cwd, "templates", "wordlist"),
        "bgmdir": os.path.join(cwd, "templates", "song"),
    }


class EmotanMW(QMainWindow):
    def __init__(self, app, args):
        QMainWindow.__init__(self)
        gui.mw = self
        self.app = app
        self.setting = default_setting()
        self._ui()
        self.mode = "View"
        self.center()
        self.show()

    def _ui(self):
        self.form = gui.forms.main.Ui_MainWindow()
        self.form.setupUi(self)
        if not isMac:
            # TODO: Check if menubar is clickable on bundled version on Mac
            # cf: http://python.6.x6.nabble.com/Bug-PyQt5-version-5-7-0-
            # OS-X-11-4-El-Capitan-MenuBar-requires-defocus-refocus-of-
            # app-to-work-Davi-td5200429.html
            self.form.menubar.setNativeMenuBar(False)
        self._ui_menu()
        self._ui_entrylist()
        self._ui_button()
        self._ui_progress()

    def _ui_menu(self):
        form = self.form
        form.actionExtract_2.triggered.connect(self._on_extract)
        form.actionPreferences.triggered.connect(self._on_preferences)
        form.actionCopy.triggered.connect(self._on_copy)
        form.actionSave.triggered.connect(self._on_save)
        form.actionOpen.triggered.connect(self._on_open)

    def _ui_button(self):
        form = self.form
        form.addButton.setIcon(QIcon('{}/plus_button_green.png'.format(ICONS)))
        form.delButton.setIcon(QIcon('{}/minus_button_red.png'.format(ICONS)))
        form.dlButton.setIcon(QIcon('{}/dl_button.png'.format(ICONS)))
        form.modeButton.setIcon(QIcon('{}/edit_button.png'.format(ICONS)))
        form.transButton.setIcon(QIcon('{}/translate_button2.png'.format(ICONS)))
        form.configButton.setIcon(QIcon('{}/config_button.png'.format(ICONS)))
        form.addButton.clicked.connect(lambda: self.entrylist.add_entry('', self.mode))
        form.delButton.clicked.connect(self.entrylist.remove_selected)
        form.dlButton.clicked.connect(self._on_download)
        form.modeButton.clicked.connect(self._on_mode_update)
        form.transButton.clicked.connect(self._on_translate)
        form.configButton.clicked.connect(self._on_tts_config)
        form.audioButton.clicked.connect(self._on_audiobook)
        form.textButton.clicked.connect(self._on_textbook)

    def _ui_entrylist(self):
        import gui.widgets.entrylist
        self.entrylist = gui.widgets.entrylist.EntryList()
        self.form.verticalLayout.insertWidget(0, self.entrylist)

    def _ui_progress(self):
        import gui.progress
        self.progress = gui.progress.ProgressManager(self)

    def basepath(self):
        return os.path.join(self.setting['workspace'], self.setting['title'])

    def _on_preferences(self):
        gui.dialogs.open("Preferences", self)

    def _on_open(self):
        import gui.open
        gui.open.on_open(self)

    def _on_save(self):
        import gui.save
        gui.save.on_save(self)

    def _on_extract(self):
        import gui.extract
        gui.extract.on_extract(self)

    def _on_mode_update(self):
        if self.mode == "View":
            # Change EntryList Mode to "Edit" and the icon to "View"
            self.form.modeButton.setIcon(QIcon("{}/disp_button.png".format(ICONS)))
            self.entrylist.update_mode("Edit")
            self.mode = "Edit"
        elif self.mode == "Edit":
            self.form.modeButton.setIcon(QIcon("{}/edit_button.png".format(ICONS)))
            self.entrylist.update_mode("View")
            self.entrylist.update_all()
            self.mode = "View"

    def _on_download(self):
        # To update 'Empty entry' if a name is added to it
        self.entrylist.update_all()
        import gui.download
        gui.download.on_download(self)

    def _on_translate(self):
        # To update 'Empty entry' if a name is added to it
        self.entrylist.update_all()
        import gui.translate
        gui.translate.on_translate(self)

    def _on_tts_config(self):
        gui.dialogs.open("Preferences", self, tab="TTS")

    def _on_audiobook(self):
        # To update 'Empty entry' if a name is added to it
        self.entrylist.update_all()
        import gui.audiodialog
        gui.audiodialog.on_audiodialog(self)

    def _on_textbook(self):
        import gui.textdialog
        gui.textdialog.on_textdialog(self)

    def _on_copy(self):
        import gui.smartcopy
        gui.smartcopy.on_copy(self)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
