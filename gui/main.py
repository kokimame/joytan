# Copyright: Koki Mametani <kokimametani@gmail.com>

from bavl.frame import FrameManager
from gui.qt import *
from gui.framelist import FrameList
from gui.bundle import BundleFactory
from gui.utils import isMac, isLin, isWin
import gui

defaultLinPref = {
    "workdir": "/home/kokimame/Emotan/workspace",
    "sfxdir": "/home/kokimame/Dropbox/Python/emotan/templates/sfx",
    "worddir": "/home/kokimame/Dropbox/Python/emotan/templates/wordlist",
    "bgmdir": "/home/kokimame/Dropbox/Python/emotan/templates/song",
    "title": "emotan-sample",
}

defaultMacPref = {
    "workdir": "/Users/Koki/Emotan/workspace",
    "sfxdir": "/Users/Koki/Dropbox/Python/emotan/templates/sfx",
    "worddir": "/Users/Koki/Dropbox/Python/emotan/templates/wordlist",
    "bgmdir": "/Users/Koki/Dropbox/Python/emotan/templates/song",
    "title": "emotan-sample",
}

class BavlMW(QMainWindow):
    def __init__(self, app, args):
        QMainWindow.__init__(self)
        gui.mw = self
        self.app = app

        self.onlineRef = "dictionary-com"
        if isLin:
            self.pref = defaultLinPref
        elif isMac:
            self.pref = defaultMacPref
        else:
            print("Sorry, Windows is now under development!")

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
        return self.pref['workdir'] + '/' + self.pref['title']

    def setupMainWindow(self):
        self.form = gui.forms.main.Ui_MainWindow()
        self.form.setupUi(self)
        self.setWindowTitle("Emotan えも単")

    def setupFrameList(self):
        framelist = FrameList(self)
        self.form.verticalLayout.addWidget(framelist)
        self.framelist = framelist

    def setupMenus(self):
        form = self.form
        form.actionExtract.triggered.connect(self.onExtract)
        form.actionPreferences.triggered.connect(self.onPreferences)

    def setupButtons(self):
        form = self.form
        form.mp3Button.clicked.connect(self.onCreateMp3)
        form.pdfButton.clicked.connect(lambda x: print("-- Under constriction --"))
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
