import gui
from gui.qt import *
from tools.downloader.gimage import GimageThread



class ImagePanel(QListWidget):

    class DlButton(QPushButton):
        def __init__(self, panel):
            super().__init__('Download')
            self.panel = panel
            self.clicked.connect(self.startDownloading)

        def startDownloading(self):
            self.dlThread = GimageThread(self.panel.group, self.panel.destDir)
            self.dlThread.finished.connect(self.uploadImages)
            self.dlThread.start()

        def uploadImages(self):
            for i in range(1, 4):
                imgpath = os.path.join(self.panel.destDir, "%d.jpg" % i)
                pixmap = QPixmap(imgpath).scaled(128, 128)
                img = QLabel()
                img.setPixmap(pixmap)
                lwi = QListWidgetItem()
                lwi.setSizeHint(img.sizeHint())
                self.panel.insertItem(self.panel.count() - 1, lwi)
                self.panel.setItemWidget(lwi, img)


    def __init__(self, group, destDir):
        super(ImagePanel, self).__init__()
        self.group = group
        self.destDir = destDir

        self.setFlow(QListView.LeftToRight)
        self.setFixedHeight(150)

        lwi = QListWidgetItem()
        dlBtn = self.DlButton(self)
        lwi.setSizeHint(dlBtn.sizeHint())
        self.addItem(lwi)
        self.setItemWidget(lwi, dlBtn)
