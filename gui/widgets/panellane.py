import gui
from gui.qt import *
from emotan.downloader.gimage import GimageThread


class Panel(QPushButton):
    _STATE_MSG = {'INIT': None,
                  'READY': 'Click to Download',
                  'WORK': 'Downloading',
                  'WAIT': 'Waiting',
                  'DONE': ''}
    FIXED_SIZE = (148, 148)

    # Emit signal to start downloading when click the 'READY' panel
    dl = pyqtSignal()

    def __init__(self, state, count):
        super().__init__()
        self.state = None
        self.count = count

        if state == 'INIT':
            self.setDisabled(True)
            self.state_manager('INIT')
        elif state == 'READY':
            self.get_ready()
        else:
            raise Exception('Invalid state "%s" o panel on initialization' % state)

    def get_ready(self):
        self.state_manager('READY')
        self.clicked.connect(self.dl.emit)

    def set_image(self, imgpath):
        pixmap = QPixmap(imgpath).scaled(*self.FIXED_SIZE)
        self.setIcon(QIcon(pixmap))
        self.setIconSize(pixmap.rect().size())
        self.state_manager('DONE')

    def state_manager(self, state):
        # if new state is
        # 'INIT': Show the index in the lane and disable clicking,
        # 'READY': Use defined message and enable clicking
        # 'WORK' and 'WAIT': Use defined message and disable clicking
        if state == 'INIT':
            self.setText('%d' % (self.count + 1))
        else:
            self.setText(self._STATE_MSG[state])

        if state in ['INIT', 'WORK', 'WAIT']:
            self.setDisabled(True)
        else:
            self.setDisabled(False)

        self.state = state


class PanelLane(QListWidget):

    def __init__(self, group, destdir, maximg):
        super(PanelLane, self).__init__()
        self.group = group
        self.destdir = destdir
        self.maximg = maximg
        self.thread = GimageThread(group, destdir)
        self.thread.done.connect(self.on_set_image)

        # Because QPixmap doesn't store the path of image they have,
        # all imgpathes in the panel are stored in this list.
        self.images = []
        self.imgcites = []

        self.setFlow(QListView.LeftToRight)
        self.setFixedHeight(150)

        for i in range(self.maximg):
            if i == 0:
                state = 'READY'
            else:
                state = 'INIT'
            panel = Panel(state, i)
            panel.dl.connect(self.on_download)
            panel.setFixedSize(*Panel.FIXED_SIZE)
            lwi = QListWidgetItem()
            lwi.setSizeHint(panel.size())
            self.addItem(lwi)
            self.setItemWidget(lwi, panel)

    def on_download(self):
        waiting = 0
        for i in range(self.count()):
            p = self._get_panel(i)
            if p.state in ['INIT', 'READY', 'WORK', 'WAIT']:
                p.state_manager('WORK')
                waiting += 1
        if waiting:
            self.thread.set_total(waiting)
            self.thread.start()

    def on_set_image(self, imgpath, link):
        # Check from left to right among panels,
        # set the new image at anything not done yet
        for i in range(self.count()):
            p = self._get_panel(i)
            if p.state != 'DONE':
                p.set_image(imgpath)
                self.images.append(imgpath)
                self.imgcites.append(link)
                break

        # Make the most left panel in inital state ready
        for i in range(self.count()):
            p = self._get_panel(i)
            if p.state == 'INIT':
                p.get_ready()
                break

    def on_wait(self):
        # Make everything but 'DONE' panel wating
        for i in range(self.count()):
            p = self._get_panel(i)
            if p.state != 'DONE':
                p.state_manager('WAIT')

    def is_waiting(self):
        waiting = 0
        for i in range(self.count()):
            p = self._get_panel(i)
            if p.state in ['INIT', 'READY', 'WORK', 'WAIT']:
                waiting += 1
        return waiting

    def set_working(self):
        for i in range(self.count()):
            p = self._get_panel(i)
            if p.state in ['INIT', 'READY', 'WORK', 'WAIT']:
                p.state_manager('WORK')


    def _get_panel(self, cnt):
        return self.itemWidget(self.item(cnt))
