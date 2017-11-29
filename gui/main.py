# Copyright: Koki Mametani <kokimametani@gmail.com>
from gui.qt import *
from gui.utils import isMac, isLin, isWin, rmdir
import gui


def defaultPref():
    import os
    cwd = os.getcwd()
    workspace = None
    tts = None

    if isLin:
        workspace = os.path.join("/home", "kokimame", "Emotan", "workspace")
        tts = "espeak"
    elif isMac:
        workspace = os.path.join("/Users", "Koki", "Emotan", "workspace")
        tts = "say"
    else:
        workspace = os.path.join("C:", "\\Users", "Koki", "Documents", "Emotan", "workspace")
        tts = "espeak"

    return {
        "workspace": workspace,
        "tts": tts,
        "sfxdir": os.path.join(cwd, "templates", "sfx"),
        "worddir": os.path.join(cwd, "templates", "wordlist"),
        "bgmdir": os.path.join(cwd, "templates", "song"),
        "title": "emotan-sample",
        "onlineSrc": "Wiktionary"
    }

class EmotanMW(QMainWindow):
    def __init__(self, app, args):
        QMainWindow.__init__(self)
        gui.mw = self
        self.app = app

        self.pref = defaultPref()
        rmdir(self.getRootPath())
        print(self.pref)

        self.initUi()
        self.entryMode = "Disp"

        self.center()
        self.show()

    def initUi(self):
        self.setupMainWindow()
        self.setupMenus()
        self.setupEntryList()
        self.setupButtons()
        self.setupProgress()

    def getRootPath(self):
        return os.path.join(self.pref['workspace'], self.pref['title'])

    def setupMainWindow(self):
        self.form = gui.forms.main.Ui_MainWindow()
        self.form.setupUi(self)

    def setupEntryList(self):
        import gui.entrylist
        self.entrylist = gui.entrylist.EntryList()
        self.form.verticalLayout.insertWidget(0, self.entrylist)

    def setupMenus(self):
        form = self.form
        # Fixme: Failed to use the original name 'actionExtract' on Qt Designer
        form.actionExtract_2.triggered.connect(self.onExtract)
        form.actionPreferences.triggered.connect(self.onPreferences)
        form.actionCopy.triggered.connect(self.onCopy)
        form.actionSave.triggered.connect(self.onSave)
        form.actionOpen.triggered.connect(self.onOpen)

    def setupButtons(self):
        form = self.form
        form.addButton.setIcon(QIcon('design/icons/plus_button_green.png'))
        form.delButton.setIcon(QIcon('design/icons/minus_button_red.png'))
        form.dlButton.setIcon(QIcon('design/icons/dl_button.png'))
        form.modeButton.setIcon(QIcon('design/icons/edit_button.png'))
        form.transButton.setIcon(QIcon('design/icons/translate_button2.png'))
        form.configButton.setIcon(QIcon('design/icons/config_button.png'))
        form.addButton.clicked.connect(lambda: self.entrylist.addEntry('', self.entryMode))
        form.delButton.clicked.connect(self.entrylist.deleteSelected)
        form.dlButton.clicked.connect(self.onDownload)
        form.modeButton.clicked.connect(self.onUpdateMode)
        form.transButton.clicked.connect(self.onTranslate)
        form.configButton.clicked.connect(self.onConfigure)
        form.audioButton.clicked.connect(self.onCreateMp3)
        form.textButton.clicked.connect(self.onCreateText)

    def setupProgress(self):
        import gui.progress
        self.progress = gui.progress.ProgressManager(self)

    def onPreferences(self):
        gui.dialogs.open("Preferences", self)

    def onOpen(self):
        import gui.open
        gui.open.onOpen(self)

    def onSave(self):
        import gui.save
        gui.save.onSave(self)

    def onExtract(self):
        import gui.extract
        gui.extract.onExtract(self)

    def onUpdateMode(self):
        if self.entryMode == "Disp":
            # Change EntryList Mode to "Edit" and the icon to "Display"
            self.form.modeButton.setIcon(QIcon("design/icons/disp_button.png"))
            self.entrylist.updateMode("Edit")
            self.entryMode = "Edit"
        elif self.entryMode == "Edit":
            self.form.modeButton.setIcon(QIcon("design/icons/edit_button.png"))
            self.entrylist.updateMode("Disp")
            self.entrylist.updateAll()
            self.entryMode = "Disp"


    def onDownload(self):
        # To update 'Empty entry' if a name is added to it
        self.entrylist.updateAll()
        import gui.download
        gui.download.onDownload(self)

    def onTranslate(self):
        # To update 'Empty entry' if a name is added to it
        self.entrylist.updateAll()
        import gui.translate
        gui.translate.onTranslate(self)

    def onConfigure(self):
        gui.dialogs.open("Preferences", self, tab="TTS")

    def onCreateMp3(self):
        # To update 'Empty entry' if a name is added to it
        self.entrylist.updateAll()
        import gui.mp3dialog
        gui.mp3dialog.onMp3Dialog(self)

    def onCreateText(self):
        import gui.textdialog
        gui.textdialog.onTextDialog(self)


    def onCopy(self):
        import gui.smartcopy
        gui.smartcopy.onCopy(self)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
