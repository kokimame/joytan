# Copyright: Koki Mametani <kokimametani@gmail.com>
from gui.qt import *
from gui.framelist import FrameList
from gui.utils import isMac, isLin, isWin, rmdir
import gui


def defaultPref():
    import os
    cwd = os.getcwd()
    workdir = None

    if isLin:
        workdir = "/home/kokimame/Emotan/workspace"
    elif isMac:
        workdir = "/Users/Koki/Emotan/workspace"
    else:
        workdir = "C:\\Users\\Koki\\Documents\\Emotan\\workspace"

    return {
        "workdir": workdir,
        "sfxdir": cwd + "/templates/sfx",
        "worddir": cwd + "/templates/wordlist",
        "bgmdir": cwd + "/templates/song",
        "title": "emotan-sample",
        "onlineRef": "Wiktionary"
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
        self.frameMode = "Disp"

        self.center()
        self.show()

    def initUi(self):
        self.setupMainWindow()
        self.setupMenus()
        self.setupFrameList()
        self.setupButtons()

    def getRootPath(self):
        return "{workdir}/{title}".format(workdir=self.pref['workdir'], title=self.pref['title'])

    def setupMainWindow(self):
        self.form = gui.forms.main.Ui_MainWindow()
        self.form.setupUi(self)

    def setupFrameList(self):
        framelist = FrameList()
        self.form.verticalLayout.insertWidget(0, framelist)
        self.framelist = framelist

    def setupMenus(self):
        form = self.form
        form.actionExtract.triggered.connect(self.onExtract)
        form.actionPreferences.triggered.connect(self.onPreferences)
        form.actionCopy.triggered.connect(self.onCopyContents)

    def setupButtons(self):
        form = self.form
        form.addButton.setIcon(QIcon('design/icons/plus_button_green.png'))
        form.delButton.setIcon(QIcon('design/icons/minus_button_red.png'))
        form.dlButton.setIcon(QIcon('design/icons/dl_button.png'))
        form.editButton.setIcon(QIcon('design/icons/edit_button.png'))
        form.transButton.setIcon(QIcon('design/icons/translate_button2.png'))
        form.configButton.setIcon(QIcon('design/icons/config_button.png'))
        form.addButton.clicked.connect(lambda: self.framelist.addBundle('', self.frameMode))
        form.delButton.clicked.connect(self.framelist.deleteBundle)
        form.dlButton.clicked.connect(self.onDownload)
        form.editButton.clicked.connect(self.onUpdateFrameMode)
        form.transButton.clicked.connect(self.onTranslate)
        form.configButton.clicked.connect(lambda: print("-- Under construction --"))
        form.audioButton.clicked.connect(self.onCreateMp3)
        form.textButton.clicked.connect(self.onCreateText)

    def onPreferences(self):
        import gui.preferences
        gui.dialogs.open("Preferences", self)

    def onExtract(self):
        import gui.extract
        gui.extract.onExtract(self)

    def onUpdateFrameMode(self):
        if self.frameMode == "Disp":
            # Change Frame Mode to "Edit" and the icon to "Display"
            self.form.editButton.setIcon(QIcon("design/icons/disp_button.png"))
            self.framelist.updateMode("Edit")
            self.frameMode = "Edit"
        elif self.frameMode == "Edit":
            self.form.editButton.setIcon(QIcon("design/icons/edit_button.png"))
            self.framelist.updateMode("Disp")
            self.framelist._update()
            self.frameMode = "Disp"


    def onDownload(self):
        if self.framelist.count() == 0:
            print("Nothing to download")
            return

        # To update 'Anonymous bundle' if a name is added to it
        self.framelist._update()
        import gui.download
        gui.download.onDownload(self)

    def onTranslate(self):
        if self.framelist.count() == 0:
            print("Nothing to translate")
            return

        # To update 'Anonymous bundle' if a name is added to it
        self.framelist._update()
        import gui.translate
        gui.translate.onTranslate(self)

    def onCreateMp3(self):
        if self.framelist.count() == 0:
            print("Nothing to create")
            return

        # To update 'Anonymous bundle' if a name is added to it
        self.framelist._update()
        import gui.mp3dialog
        gui.mp3dialog.onMp3Dialog(self)

    def onCreateText(self):
        if self.framelist.count() == 0:
            print("Nothing to get text")
            return
        self.framelist._update()
        import gui.textdialog
        gui.textdialog.onTextDialog(self)


    def onCopyContents(self):
        if self.framelist.count() == 0:
            print("Nothing to copy")
            return
        self.framelist.copyContents()
        self.framelist._update()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
