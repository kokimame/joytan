from PyQt5.QtMultimedia import QMediaPlayer

import gui
from gui.qt import *
from tools.handler import mp3handler
from gui.utils import getFileNameFromPath


class MediaPlayer(QMediaPlayer):
    def __init__(self, parent):
        super(MediaPlayer, self).__init__()
        self.stateChanged.connect(parent.iconChange)

    def playContent(self, content):
        if not self.state(): # default state is 0 (Audio stopped)
            self.setMedia(content)
            self.play()
        else:
            self.stop()


class Mp3Widget(QWidget):
    def __init__(self, mp3path, groupIdx, delTrigger, lwi):
        super(Mp3Widget, self).__init__()
        self.mp = MediaPlayer(self)
        # Store path as raw string otherwise causes bug on concatenation
        self.mp3path = mp3path
        self.gidx = groupIdx
        self.delTrigger = delTrigger
        self.lwi = lwi      # ListWidgetItem that contains this widget
        self.filename = getFileNameFromPath(mp3path)
        self.hhmmss = mp3handler.getMp3Duration(mp3path)
        self.content = QMediaContent(QUrl.fromLocalFile(mp3path))

        self.initUi()

    def initUi(self):
        delBtn = QPushButton()
        delBtn.setIcon(QIcon("design/icons/delete_button.png"))
        delBtn.clicked.connect(lambda: self.delTrigger(self.lwi))
        label = QLabel("{name} {hhmmss}".
                       format(name=self.filename, hhmmss=self.hhmmss))
        self.playBtn = QPushButton("Play")
        self.playBtn.clicked.connect(lambda: self.mp.playContent(self.content))
        volSld = QSlider(Qt.Horizontal)
        volSld.setFixedWidth(90)
        volSld.setRange(0, 100)
        volSld.setValue(100)
        volSld.valueChanged.connect(self.mp.setVolume)

        hbox = QHBoxLayout()
        hbox.addWidget(delBtn)
        hbox.addWidget(label)
        hbox.addWidget(self.playBtn)
        hbox.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hbox.addWidget(volSld)

        self.setLayout(hbox)

    def iconChange(self, state):
        if state:
            self.playBtn.setText("Stop")
        else:
            self.playBtn.setText("Play")


    def forceStop(self):
        self.mp.stop()