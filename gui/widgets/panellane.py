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
        self.clicked.connect(self.dl.emit)
        self.state_manager(state)

    def set_image(self, imgpath):
        pixmap = QPixmap(imgpath).scaled(*self.FIXED_SIZE)
        self.setIcon(QIcon(pixmap))
        self.setIconSize(pixmap.rect().size())
        self.state_manager('DONE')

    def state_manager(self, state):
        # List of state:
        # 'INIT': Initial state. Show the index in the lane and disable clicking,
        # 'READY': Ready-to-download. Use defined message and enable clicking
        # 'WORK' Downloading in process. Use defined message and disable clicking
        # 'WAIT': Waiting for download thread. Use defined message and disable clicking
        # 'DONE': Image successfully downloaded and set. Enable right clicking.
        if state == 'INIT':
            self.setText('%d' % (self.count + 1))
            self.setDisabled(True)
        elif state == 'READY':
            self.setText(self._STATE_MSG[state])
            self.setDisabled(False)
        elif state == 'WORK':
            self.setText(self._STATE_MSG[state])
            self.setDisabled(True)
        elif state == 'WAIT':
            self.setText(self._STATE_MSG[state])
            self.setDisabled(True)
        elif state == 'DONE':
            self.setText(self._STATE_MSG[state])
            self.setDisabled(False)
        else:
            raise Exception("Invalid Panel state %s" % state)

        self.state = state


class PanelLane(QListWidget):

    def __init__(self, group, following, destdir, maximg):
        super(PanelLane, self).__init__()
        self.group = group
        self.destdir = destdir
        self.maximg = maximg
        self.thread = GimageThread(' '.join([self.group, following]), destdir)
        self.thread.upload.connect(self.on_set_image)
        self.thread.finished.connect(self.on_finish_working)

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

    def _debug_panel_state(self):
        for i in range(self.count()):
            p = self._get_panel(i)
            print(p.state, end='  ')
        print()

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

    @pyqtSlot(str)
    def on_update_following(self, following):
        self.thread.update_keyword(' '.join([self.group, following]))

    @pyqtSlot()
    def on_finish_working(self):
        first = True
        for i in range(self.count()):
            p = self._get_panel(i)
            if p.state  == 'WORK':
                if first == True:
                    p.state_manager('READY')
                    first = False
                else:
                    p.state_manager('INIT')
            elif p.state == 'WAIT':
                raise Exception("Thread finishes in invalid time. (Some of panel is still waiting)")

    def is_waiting(self):
        waiting = 0
        for i in range(self.count()):
            p = self._get_panel(i)
            if p.state in ['INIT', 'READY', 'WORK', 'WAIT']:
                waiting += 1
        return waiting

    def start_working(self):
        for i in range(self.count()):
            p = self._get_panel(i)
            if p.state in ['INIT', 'READY', 'WORK', 'WAIT']:
                p.state_manager('WORK')

    def _get_panel(self, cnt):
        return self.itemWidget(self.item(cnt))
