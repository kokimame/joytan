import gui
from gui.qt import *
from gui.utils import path2filename
from gui.widgets.entry import Editor


class MediaPlayer(QMediaPlayer):

    def __init__(self, parent):
        super(MediaPlayer, self).__init__()
        self.stateChanged.connect(parent.on_icon_change)

    def play_content(self, content):
        if not self.state(): # default state is 0 (Audio stopped)
            self.setMedia(content)
            self.play()
        else:
            self.stop()


class FlowItem(QWidget):

    delete = pyqtSignal()

    def __init__(self):
        super(FlowItem, self).__init__()
        self.setLayout(self._ui())

    def _ui(self):
        title = QLabel()
        title.setMinimumHeight(30)
        volume = QSlider(Qt.Horizontal)
        volume.setObjectName("volume")
        volume.setFixedWidth(90)
        volume.setRange(0, 100)
        volume.setValue(100)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(title)
        hbox.addWidget(volume)
        return hbox

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self._click_menu()
        elif event.button() == Qt.LeftButton:
            super().mousePressEvent(event)

    def _click_menu(self):
        m = QMenu()
        a = m.addAction("Delete")
        a.triggered.connect(lambda: self.delete.emit())

        m.exec_(QCursor.pos())


class Rest(FlowItem):

    def __init__(self):
        super(Rest, self).__init__()

    def _ui(self):
        layout = super(Rest, self)._ui()
        title = layout.itemAt(0).widget()
        volume = layout.itemAt(1).widget()

        title.setText("Silence")
        volume.setDisabled(True)
        duration = QDoubleSpinBox()
        duration.setObjectName("duration")
        duration.setSuffix(" sec")
        duration.setValue(1.0)
        duration.setSingleStep(0.5)

        layout.addWidget(duration)
        return layout

    def get_duration(self):
        duration = self.findChild(QDoubleSpinBox, "duration")
        return duration.value()


class Mp3Object(FlowItem):

    def __init__(self, mp3path):
        self.mp3path = mp3path
        self.content = QMediaContent(QUrl.fromLocalFile(mp3path))
        self.mp = MediaPlayer(self)
        super(Mp3Object, self).__init__()

    def _ui(self):
        layout = super(Mp3Object, self)._ui()
        title = layout.itemAt(0).widget()
        volume = layout.itemAt(1).widget()

        title.setText(path2filename(self.mp3path))
        title.setStyleSheet("background-color : rgb(255,130,90)")
        volume.valueChanged.connect(self.mp.setVolume)
        play_btn = QPushButton("Play")
        play_btn.clicked.connect(lambda: self.mp.play_content(self.content))
        play_btn.setObjectName("play_btn")
        layout.addWidget(play_btn)
        return layout

    def on_icon_change(self, state):
        play_btn = self.findChild(QPushButton, "play_btn")
        if state:
            play_btn.setText("Stop")
        else:
            play_btn.setText("Play")

    def force_stop(self):
        self.mp.stop()


# An object corresponds to ewkey in EntryWidget
class EwkeyObject(FlowItem):

    def __init__(self, ewkey):
        self.ewkey = ewkey
        super(EwkeyObject, self).__init__()

    def _ui(self):
        layout = super(EwkeyObject, self)._ui()
        title = layout.itemAt(0).widget()
        volume = layout.itemAt(1).widget()

        title.setText(self.ewkey)
        ks = self.ewkey.split('-')
        if 'atop' in ks:
            title.setStyleSheet(Editor.COLOR['atop'])
        elif 'def' in ks:
            title.setStyleSheet(Editor.COLOR['def'])
        elif 'ex' in ks:
            title.setStyleSheet(Editor.COLOR['ex'])
        else:
            raise Exception("Wrong ewkey")
        return layout


class Index(FlowItem):

    def __init__(self):
        super(Index, self).__init__()

    def _ui(self):
        layout = super(Index, self)._ui()
        title = layout.itemAt(0).widget()
        volume = layout.itemAt(1).widget()

        title.setText('Index')
        title.setStyleSheet("background-color : rgb(130,255,90)")
        return layout
