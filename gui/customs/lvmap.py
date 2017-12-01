import gui
from gui.qt import *
from tools.speaker import Speaker
from gui.utils import LANGUAGES, LANGCODES

class LvMapWidget(QWidget):
    # Maps from content type and language code and Voice ID, and test sample text-to-speech
    def __init__(self, tts, label, lv):
        super(LvMapWidget, self).__init__()
        self.tts = Speaker[tts]
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
