# Copyright: Koki Mametani <kokimametani@gmail.com>

from bavl.frame import FrameManager
from gui.qt import *
from gui.framelist import FrameList
from gui.bundle import BundleFactory
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
        print("Sorry only support Mac and Linux for now.")
        exit(1)

    return {
        "workdir": workdir,
        "sfxdir": cwd + "/templates/sfx",
        "worddir": cwd + "/templates/wordlist",
        "bgmdir": cwd + "/templates/song",
        "title": "emotan-sample",
        "onlineRef": "Dictionary.com"
    }

class BavlMW(QMainWindow):
    def __init__(self, app, args):
        QMainWindow.__init__(self)
        gui.mw = self
        self.app = app

        self.pref = defaultPref()
        rmdir(self.getRootPath())
        print(self.pref)

        self.fm = FrameManager(self)
        self.bdfactory = BundleFactory()
        self.initUi()


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
        self.setWindowTitle("Emotan えも単")

    def setupFrameList(self):
        framelist = FrameList(self)
        self.form.verticalLayout.insertWidget(0, framelist)
        self.framelist = framelist

    def setupMenus(self):
        form = self.form
        form.actionExtract.triggered.connect(self.onExtract)
        form.actionPreferences.triggered.connect(self.onPreferences)

    def setupButtons(self):
        form = self.form
        form.addButton.setIcon(QIcon('design/icons/plus_button_green.png'))
        form.delButton.setIcon(QIcon('design/icons/minus_button_red.png'))
        form.editButton.setIcon(QIcon('design/icons/edit_button.png'))
        form.configButton.setIcon(QIcon('design/icons/config_button.png'))
        form.mp3Button.clicked.connect(self.onCreateMp3)
        form.pdfButton.clicked.connect(lambda x: print("-- Under construction --"))
        form.dlcButton.clicked.connect(self.onDownload)

    def onPreferences(self):
        import gui.preferences
        gui.dialogs.open("Preferences", self)

    def onExtract(self):
        import gui.extract
        gui.extract.onExtract(self)

    def onDownload(self):
        import gui.download
        gui.download.onDownload(self)

    def onCreateMp3(self):
        import gui.mp3dialog
        gui.mp3dialog.onMp3Dialog(self)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
