import gui
from gui.qt import *
from tools.downloader.gimage import GimageThread



class ImagePanel(QListWidget):

    class DlButton(QPushButton):
        def __init__(self, panel):
            super().__init__('Click to Download')
            self.panel = panel
            self.dlThread = GimageThread(panel.group, panel.destDir)
            self.clicked.connect(self.startThread)
            self.dlThread.finished.connect(self.threadFinished)

        def startThread(self):
            panel = self.panel
            capa = panel.getCapacity()
            if capa >= 1:
                print(capa)
                self.dlThread.sig.connect(self.uploadImage)
                self.dlThread.setImgNumber(capa)
                self.dlThread.start()
                self.setText("Downloading")
                self.setEnabled(False)

        def uploadImage(self, imgfile):
            pixmap = QPixmap(imgfile).scaled(128, 128)
            img = QLabel()
            img.setPixmap(pixmap)
            lwi = QListWidgetItem()
            lwi.setSizeHint(img.sizeHint())
            self.panel.insertItem(self.panel.count() - 1, lwi)
            self.panel.setItemWidget(lwi, img)
            self.panel.images.append(imgfile)

        def threadFinished(self):
            self.setText('Click to Download')
            self.setEnabled(True)


    def __init__(self, group, destDir, maxImg):
        super(ImagePanel, self).__init__()
        self.group = group
        self.destDir = destDir
        self.maxImg = maxImg
        # Because QPixmap doesn't store the path of image they have,
        # all imgpathes in the panel are stored in this list.
        self.images = []

        self.setFlow(QListView.LeftToRight)
        self.setFixedHeight(150)

        lwi = QListWidgetItem()
        dlBtn = self.DlButton(self)
        lwi.setSizeHint(dlBtn.sizeHint())
        self.addItem(lwi)
        self.setItemWidget(lwi, dlBtn)

    def getCapacity(self):
        print(self.maxImg, self.count())
        return self.maxImg - self.count() + 1
