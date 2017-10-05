# Copyright: Koki Mametani <kokimametani@gmail.com>

from bavl.frame import FrameManager
from gui.qt import *
from gui.framelist import FrameList
from gui.utils import isMac, isLin, isWin
import gui

class BavlMW(QMainWindow):
    def __init__(self, app, args):
        QMainWindow.__init__(self)
        gui.mw = self
        self.app = app

        self.fm = FrameManager()

        try:
            self.initUi()
        except Exception as e:
            print("Error occurred on initUI", e)
            sys.exit(1)

        self.center()
        self.show()

    def initUi(self):
        self.setupMainWindow()
        self.setupMenus()
        self.setupFrameList()
        self.setupButtons()

    def setupMainWindow(self):
        self.form = gui.forms.main.Ui_MainWindow()
        self.form.setupUi(self)
        self.setWindowTitle("Emotan えも単")

    def setupFrameList(self):
        framelist = FrameList(self.fm)
        self.form.verticalLayout.addWidget(framelist)
        self.framelist = framelist

    def setupMenus(self):
        form = self.form
        form.actionExtract.triggered.connect(self.onExtract)
        form.actionPreferences.triggered.connect(self.onPreferences)

    def setupButtons(self):
        form = self.form
        form.mp3Button.clicked.connect(self.onMp3Compile)
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

    def onMp3Compile(self):
        import gui.mp3dialog
        gui.mp3dialog.onMp3Dialog(self)

    def onMp3Convert(self):
        pass

    def onPdfConvert(self):
        pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
