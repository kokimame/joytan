import gui
from gui.qt import *
from emotan.downloader.gimage import GimageThread


class ImagePanel(QListWidget):

    class DlButton(QPushButton):
        def __init__(self, panel):
            super().__init__('Click to Download')
            self.panel = panel
            self.dl_thread = GimageThread(panel.group, panel.destdir)
            self.clicked.connect(self._on_threading)
            self.dl_thread.finished.connect(self._on_thread_end)

        def _on_threading(self):
            panel = self.panel
            capa = panel.get_capacity()
            if capa >= 1:
                print(capa)
                self.dl_thread.sig.connect(self._on_image_upload)
                self.dl_thread.set_total(capa)
                self.dl_thread.start()
                self.setText("Downloading")
                self.setEnabled(False)

        def _on_image_upload(self, imgfile):
            pixmap = QPixmap(imgfile).scaled(128, 128)
            img = QLabel()
            img.setPixmap(pixmap)
            lwi = QListWidgetItem()
            lwi.setSizeHint(img.sizeHint())
            self.panel.insertItem(self.panel.count() - 1, lwi)
            self.panel.setItemWidget(lwi, img)
            self.panel.images.append(imgfile)

        def _on_thread_end(self):
            self.setText('Click to Download')
            self.setEnabled(True)

    def __init__(self, group, destdir, maximg):
        super(ImagePanel, self).__init__()
        self.group = group
        self.destdir = destdir
        self.maximg = maximg
        # Because QPixmap doesn't store the path of image they have,
        # all imgpathes in the panel are stored in this list.
        self.images = []

        self.setFlow(QListView.LeftToRight)
        self.setFixedHeight(150)

        lwi = QListWidgetItem()
        dlbtn = self.DlButton(self)
        lwi.setSizeHint(dlbtn.sizeHint())
        self.addItem(lwi)
        self.setItemWidget(lwi, dlbtn)

    def get_capacity(self):
        print(self.maximg, self.count())
        return self.maximg - self.count() + 1
