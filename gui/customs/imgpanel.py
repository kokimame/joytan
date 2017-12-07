import gui
from gui.qt import *
from tools.downloader.gimage import GimageThread



class ImagePanel(QListWidget):

    class DlButton(QPushButton):
        def __init__(self, panel):
            super().__init__('Download')
            self.panel = panel
            self.dlThread = GimageThread(self.panel.group,
                                         self.panel.destDir, self.panel.maxImg)
            self.dlThread.sig.connect(self.uploadImage)
            self.clicked.connect(self.startThread)

        def startThread(self):
            self.dlThread.start()

        def uploadImage(self, imgfile):
            pixmap = QPixmap(imgfile).scaled(128, 128)
            img = QLabel()
            img.setPixmap(pixmap)
            lwi = QListWidgetItem()
            lwi.setSizeHint(img.sizeHint())
            self.panel.insertItem(self.panel.count() - 1, lwi)
            self.panel.setItemWidget(lwi, img)
            self.panel.images.append(imgfile)


    def __init__(self, group, destDir, maxImg):
        super(ImagePanel, self).__init__()
        self.group = group
        self.destDir = destDir
        self.maxImg = maxImg
        self.images = []

        self.setFlow(QListView.LeftToRight)
        self.setFixedHeight(150)

        lwi = QListWidgetItem()
        dlBtn = self.DlButton(self)
        lwi.setSizeHint(dlBtn.sizeHint())
        self.addItem(lwi)
        self.setItemWidget(lwi, dlBtn)
