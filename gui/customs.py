# This line may not be in use but should be regarding with module importing of pyinstaller
from PyQt5.QtMultimedia import QMediaPlayer

from tools.cmder.mp3cmder import mp3Duration, getMp3Info
from gui.qt import *
from gui.utils import getFileNameFromPath
from tools.talker import Talkers
from gui.utils import LANGUAGES, LANGCODES

class LvMapWidget(QWidget):
    # Maps from content type and language code and Voice ID, and test sample text-to-speech
    def __init__(self, tts, label, lv):
        super(LvMapWidget, self).__init__()
        self.tts = Talkers[tts]
        # Label for content section such as 'name' and 'def-x'
        self.label = label
        # Language and Voice ID for the label (e.g, 'name' or 'def-x' etc)
        self.lv = lv
        self.initUi()

    def initUi(self):
        lbl = QLabel('%s:' % self.label.title())
        self.langCombo = QComboBox()
        self.langCombo.addItems(sorted([lang.title() for lang in LANGUAGES.values()]))
        self.langCombo.setCurrentText(LANGUAGES[self.lv[0]].title())
        self.langCombo.currentTextChanged.connect(self.updateVoiceCombo)
        lbl2 = QLabel('Voice:')
        self.voiceCombo = QComboBox()
        self.voiceCombo.addItems([name for name in self.tts.code2Vids[self.lv[0]]])

        # If a voice id is already specified for a given content section,
        # search and set the according combobox label from the given TTS's code2Vids dictionary
        if self.lv[1]:
            for combo in self.tts.code2Vids[self.lv[0]]:
                if self.tts.code2Vids[self.lv[0]][combo] == self.lv[1]:
                    self.voiceCombo.setCurrentText(combo)
        self.testBtn = QPushButton('Test')
        self.testBtn.clicked.connect(self.testVoice)

        lh = QHBoxLayout()
        lh.addWidget(lbl)
        lh.addWidget(self.langCombo)
        lh.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        vh = QHBoxLayout()
        vh.addWidget(lbl2)
        vh.addWidget(self.voiceCombo)
        vh.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        vh.addWidget(self.testBtn)
        hbox = QVBoxLayout()
        hbox.addLayout(lh)
        hbox.addLayout(vh)
        self.setLayout(hbox)

    def updateVoiceCombo(self):
        self.lv[0] = LANGCODES[self.langCombo.currentText().lower()]
        self.voiceCombo.clear()
        self.voiceCombo.addItems([name for name in self.tts.code2Vids[self.lv[0]]])
        self.voiceCombo.repaint()

    def testVoice(self):
        class PreviewThread(QThread):
            def __init__(self, parent):
                QThread.__init__(self)
                self.parent = parent

            def run(self):
                p = self.parent
                p.tts().preview(p.tts.code2Vids[p.lv[0]][p.voiceCombo.currentText()])

        # The thread must be stored under the self,
        # otherwise the thread gets destroyed while it's running, then crushes the app.
        self.pt = PreviewThread(self)
        self.pt.start()

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
        self.hhmmss = mp3Duration(mp3path)
        self.duration, self.fskhz, self.bitkbs = getMp3Info(mp3path)
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

class GroupButton(QPushButton):
    def __init__(self, trigger, group=None, idx=None):
        super(GroupButton, self).__init__()
        self.trigger = trigger
        self.group = group
        self.idx = idx
        self.initUi()

    def initUi(self):
        self.setStyleSheet("QPushButton { background-color: rgb(200,200,200); "
                             "Text-align: left; }")
        if not self.group.isupper():
            group = self.group.title()
        else:
            group = self.group
        self.setText("+ {group}".format(group=group))
        self.clicked.connect(lambda: self.trigger(idx=self.idx))