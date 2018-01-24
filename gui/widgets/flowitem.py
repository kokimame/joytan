# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Koki Mametani <kokimametani@gmail.com>
# License: GPLv3 or later; http://www.gnu.org/licenses/gpl.html


import gui
from gui import ICONS
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
    """
    Base widget of widgets shown in ListWidget for making audio-flow and
    looped BGM on audiodialog.
    """
    FIXED_WIDTH = dict(title=120,
                       postrest=165,
                       volume=100,
                       x_label=10,
                       repeat=40,
                       rep_label=50,
                       placeholder=28)

    # Abstract layout from left to right to get the index of
    # each item by LAYOUT.index('item')
    LAYOUT = ['title', 'postrest', 'volume', 'x_label',
              'repeat', 'rep_label', 'placeholder']

    delete = pyqtSignal()

    def __init__(self):
        super(FlowItem, self).__init__()
        self.setLayout(self._ui())

    def _ui(self):
        title = QLabel()
        title.setMinimumHeight(30)
        title.setFixedWidth(self.FIXED_WIDTH['title'])

        postrest = QDoubleSpinBox()
        postrest.setSuffix(" sec [post-rest]")
        postrest.setValue(0.5)
        postrest.setSingleStep(0.5)
        postrest.setObjectName("postrest")
        postrest.setFixedWidth(self.FIXED_WIDTH['postrest'])

        volume = QSlider(Qt.Horizontal)
        volume.setRange(0, 100)
        volume.setValue(100)
        volume.setFixedWidth(self.FIXED_WIDTH['volume'])

        # Label of 'x' (How many 'times')
        x_label = QLabel("x")
        x_label.setFixedWidth(self.FIXED_WIDTH['x_label'])

        repeat = QSpinBox()
        repeat.setValue(1)
        repeat.setRange(1, 99)
        repeat.setObjectName("repeat")
        repeat.setFixedWidth(self.FIXED_WIDTH['repeat'])

        rep_label = QLabel("repeat")
        rep_label.setFixedWidth(self.FIXED_WIDTH['rep_label'])

        # Placeholder of Play Button which is implemented only in Mp3Object.
        # This empty label is here for alignment.
        placeholder = QLabel("")
        placeholder.setFixedWidth(self.FIXED_WIDTH['placeholder'])

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(1)
        hbox.addWidget(title)
        hbox.addWidget(postrest)
        hbox.addWidget(volume)
        hbox.addWidget(x_label)
        hbox.addWidget(repeat)
        hbox.addWidget(rep_label)
        hbox.addWidget(placeholder)
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

    def index(self, widget_name):
        try:
            return self.LAYOUT.index(widget_name)
        except:
            raise AttributeError("Failed to find widget with name.", widget_name)

    def get_repeat(self):
        return self.findChild(QSpinBox, "repeat").value()

    def get_postrest(self):
        return self.findChild(QDoubleSpinBox, "postrest").value()

    def eliding_label_text(self, label, text):
        """
        Set elided text to given label 
        """
        matrix = QFontMetrics(label.font())
        clipped_text = matrix.elidedText(text, Qt.ElideRight, label.width())
        label.setText(clipped_text)

    def data(self):
        raise NotImplementedError


class Rest(FlowItem):
    """
    Makes an interval of silence in a-capella or looped BGM.
    Rest is appended to other FlowItem by default as postrest,
    so you don't need to add this independent Rest if you don't
    use repeating function of FlowItem. If you repeat it,
    you may want to make another silent interval at the end 
    which varies from the interval between each repetition.
    """

    def __init__(self):
        super(Rest, self).__init__()

    def _ui(self):
        layout = super(Rest, self)._ui()
        title = layout.itemAt(self.index("title")).widget()
        postrest = layout.itemAt(self.index("postrest")).widget()
        volume = layout.itemAt(self.index("volume")).widget()
        repeat = layout.itemAt(self.index("repeat")).widget()

        self.eliding_label_text(title, "Rest")
        postrest.setSuffix(" sec")
        postrest.setValue(1.0)
        volume.setDisabled(True)
        repeat.setDisabled(True)

        return layout

    def _get_duration(self):
        duration = self.findChild(QDoubleSpinBox, "duration")
        return duration.value()

    def data(self):
        return dict(
            desc="REST",
            postrest=self.get_postrest(),
        )


class Mp3Object(FlowItem):
    """
    Adds new mp3 file, such as sound effects or BGM, to an audiobook.
    """

    def __init__(self, mp3path):
        self.mp3path = mp3path
        self.content = QMediaContent(QUrl.fromLocalFile(mp3path))
        self.mp = MediaPlayer(self)
        self.stop_icon = QIcon('{}/stop_button.png'.format(ICONS))
        self.play_icon = QIcon('{}/play_button.png'.format(ICONS))
        super(Mp3Object, self).__init__()

    def _ui(self):
        layout = super(Mp3Object, self)._ui()
        title = layout.itemAt(self.index("title")).widget()
        volume = layout.itemAt(self.index("volume")).widget()
        # Remove placeholder from FlowItem layout
        layout.takeAt(self.index("placeholder"))

        title.setStyleSheet("background-color : rgb(255,130,90)")
        self.eliding_label_text(title, path2filename(self.mp3path))
        volume.valueChanged.connect(self.mp.setVolume)
        play_btn = QPushButton()
        play_btn.setFixedWidth(self.FIXED_WIDTH['placeholder'])
        play_btn.setIcon(self.play_icon)
        play_btn.clicked.connect(lambda: self.mp.play_content(self.content))
        play_btn.setObjectName("play_btn")
        layout.addWidget(play_btn)
        return layout

    def on_icon_change(self, state):
        play_btn = self.findChild(QPushButton, "play_btn")
        if state:
            play_btn.setIcon(self.stop_icon)
        else:
            play_btn.setIcon(self.play_icon)

    def force_stop(self):
        self.mp.stop()

    def data(self):
        return dict(
            desc="MP3",
            path=self.mp3path,
            volume=self.mp.volume(),
            repeat=self.get_repeat(),
            postrest=self.get_postrest(),
        )


class EwkeyObject(FlowItem):
    """
    Adds new Text-to-Speech segements in EntryWidget
    """

    def __init__(self, ewkey):
        self.ewkey = ewkey
        super(EwkeyObject, self).__init__()

    def _ui(self):
        layout = super(EwkeyObject, self)._ui()
        title = layout.itemAt(self.index("title")).widget()

        self.eliding_label_text(title, self.ewkey)
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

    def data(self):
        volume = self.layout().itemAt(2).widget()
        return dict(
            desc=self.ewkey,
            repeat=self.get_repeat(),
            volume=volume.value(),
            postrest=self.get_postrest(),
        )


class Index(FlowItem):

    def __init__(self):
        super(Index, self).__init__()

    def _ui(self):
        layout = super(Index, self)._ui()
        title = layout.itemAt(self.index("title")).widget()

        title.setText('Index')
        title.setStyleSheet("background-color : rgb(130,255,90)")
        return layout

    def data(self):
        volume = self.layout().itemAt(2).widget()
        return dict(
            desc="INDEX",
            repeat=self.get_repeat(),
            volume=volume.value(),
            postrest=self.get_postrest(),
        )
