import gui
from gui.qt import *
from emotan.handler import mp3handler
from gui.utils import path2filename


class MediaPlayer(QMediaPlayer):
    def __init__(self, parent):
        super(MediaPlayer, self).__init__()
        self.stateChanged.connect(parent.iconChange)

    def play_content(self, content):
        if not self.state(): # default state is 0 (Audio stopped)
            self.setMedia(content)
            self.play()
        else:
            self.stop()


class BarPlayer(QWidget):
    sig = pyqtSignal(str, QListWidgetItem)

    def __init__(self, mp3path, group, lwi):
        super(BarPlayer, self).__init__()
        self.mp = MediaPlayer(self)
        # Store path as raw string otherwise causes bug on concatenation
        self.mp3path = mp3path
        self.group = group
        self.lwi = lwi      # ListWidgetItem that contains this widget
        self.filename = path2filename(mp3path)
        self.hhmmss = mp3handler.get_duration(mp3path)
        self.content = QMediaContent(QUrl.fromLocalFile(mp3path))

        self.setLayout(self._ui())

    def _ui(self):
        del_btn = QPushButton()
        del_btn.setIcon(QIcon("design/icons/delete_button.png"))
        del_btn.clicked.connect(lambda: self.sig.emit(self.group, self.lwi))
        label = QLabel("{name} {hhmmss}".
                       format(name=self.filename, hhmmss=self.hhmmss))
        play_btn = QPushButton("Play")
        play_btn.clicked.connect(lambda: self.mp.play_content(self.content))
        play_btn.setObjectName("play_btn")
        volume = QSlider(Qt.Horizontal)
        volume.setFixedWidth(90)
        volume.setRange(0, 100)
        volume.setValue(100)
        volume.valueChanged.connect(self.mp.setVolume)

        hbox = QHBoxLayout()
        hbox.addWidget(del_btn)
        hbox.addWidget(label)
        hbox.addWidget(play_btn)
        hbox.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hbox.addWidget(volume)

        return hbox

    def iconChange(self, state):
        play_btn = self.findChild(QPushButton, "play_btn")
        if state:
            play_btn.setText("Stop")
        else:
            play_btn.setText("Play")


    def force_stop(self):
        self.mp.stop()