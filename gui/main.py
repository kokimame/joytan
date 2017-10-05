# Copyright: Koki Mametani <kokimametani@gmail.com>

from bavl.frame import FrameManager
from gui.qt import *
from gui.bundle import *
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
        self.setupButtons()

    def updateFrameList(self):
        for bundle in self.fm.getBundlesToRender():
            bui, bitui = BundleUi(), BundleItemUi(self.fm, bundle)
            bui.setSizeHint(bitui.sizeHint())
            self.form.frameList.addItem(bui)
            self.form.frameList.setItemWidget(bui, bitui)
            self.fm.setToRenderState(bundle, False)

    def updateBundleItemUi(self):
        mw = self.form
        for i in range(mw.frameList.count()):
            bitui = mw.frameList.itemWidget(mw.frameList.item(i))
            if bitui.toUpdate():
                bitui.updateEditors()

    def setupMainWindow(self):
        self.form = gui.forms.main.Ui_MainWindow()
        self.form.setupUi(self)
        self.setWindowTitle("Emotan えも単")

    def setupMenus(self):
        mw = self.form
        mw.actionExtract.triggered.connect(self.onExtract)
        mw.actionPreferences.triggered.connect(self.onPreferences)

    def setupButtons(self):
        mw = self.form
        mw.mp3Button.clicked.connect(self.onMp3Compile)
        mw.pdfButton.clicked.connect(lambda x: print("-- Under constriction --"))
        mw.dlcButton.clicked.connect(self.onDownload)

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
