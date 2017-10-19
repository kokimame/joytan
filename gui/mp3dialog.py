from gui.qt import *
import gui
from gui.utils import getFile, getFileNameFromPath, isLin, isMac, processCoreEvents
from tools.cmder.mp3cmder import mp3Duration, hhmmss2secCmd, getMp3Info

def onMp3Dialog(mw):
    gui.dialogs.open("Mp3Dialog", mw)


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
    def __init__(self, mp3path, parent=None):
        super(Mp3Widget, self).__init__(parent)
        self.mp = MediaPlayer(self)
        self.mp3path = mp3path
        self.filename = getFileNameFromPath(mp3path)
        self.hhmmss = mp3Duration(mp3path)
        self.duration, self.fskhz, self.bitkbs = getMp3Info(mp3path)
        self.content = QMediaContent(QUrl.fromLocalFile(mp3path))

        self.initUi()

    def initUi(self):
        label = QLabel("{name} {hhmmss}".
                       format(name=self.filename, hhmmss=self.hhmmss))
        self.playBtn = QPushButton("Play")
        self.playBtn.clicked.connect(lambda: self.mp.playContent(self.content))
        volSld = QSlider(Qt.Horizontal)
        volSld.setRange(0, 100)
        volSld.setValue(100)
        volSld.valueChanged.connect(self.mp.setVolume)

        hbox = QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(self.playBtn)
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



class Mp3Dialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.framelist = mw.framelist
        self.form = gui.forms.mp3dialog.Ui_Mp3Dialog()
        self.form.setupUi(self)
        self.setupButton()
        self.setupComboBox()
        self.setupSfxList()
        self.setupBgmList()
        self.show()

    def setupSfxList(self):
        sfxList = self.form.sfxList
        sfxList.setStyleSheet("""
                              QListWidget::item { border-bottom: 1px solid black; }
                              QListWidget::item { background-color: rgb(200,200,200); }
                              """)
        groups = ['word', 'definition', 'example']
        self.sfxCnt = [1] * len(groups)
        for i, group in enumerate(groups):
            lw, gb = QListWidgetItem(), GroupButton(self.onSfxClicked, group=group, idx=i)
            lw.setSizeHint(gb.sizeHint())
            sfxList.addItem(lw)
            sfxList.setItemWidget(lw, gb)


    def setupBgmList(self):
        bgmList = self.form.bgmList
        bgmList.setStyleSheet("""
                              QListWidget::item { border-bottom: 1px solid black; }
                              QListWidget::item { background-color: rgb(200,200,200); }
                              """)
        lw, gb = QListWidgetItem(), GroupButton(self.onBgmClicked, group="BGM")
        lw.setSizeHint(gb.sizeHint())
        bgmList.addItem(lw)
        bgmList.setItemWidget(lw, gb)

    def setupButton(self):
        form = self.form
        form.createBtn.clicked.connect(self.onCreate)
        form.cancelBtn.clicked.connect(self.reject)

    def setupComboBox(self):
        form = self.form
        if isMac:
            form.ttsCombo.setCurrentIndex(0)
        if isLin:
            form.ttsCombo.setCurrentIndex(1)

    def onCreate(self):
        form = self.form
        isGstatic = form.gstaticCheck.isChecked()
        setting = {}
        setting['repeat'] = form.wordSpin.value()

        sfxdir = {}
        for item in self.sfxGroup:
            # SFXs for a group shown in column 0
            group = item.text(0)
            sfxdir[group] = []
            for i in range(item.childCount()):
                child = item.child(i)
                sfxdir[group].append({
                    "path": child.mp3path,
                    "filename": child.filename,
                    "duration": child.duration,
                    "sampling": child.fskhz,
                    "bitrate": child.bitkbs
                })
        setting['sfx'] = sfxdir

        bgmloop = []
        for i in range(form.bgmList.count()):
            item = form.bgmList.item(i)
            bgmloop.append({"path": item.mp3path,
                            "filename": item.filename,
                            "duration": item.duration,
                            "sampling": item.fskhz,
                            "bitrate": item.bitkbs,})
        setting['loop'] = bgmloop


        from tools.cmder.mp3cmder import Mp3Cmder
        from gui.progress import ProgressDialog

        # Fixme: Here is the wrong progress length assumption!
        pd = ProgressDialog(self.framelist.count() * 3, msg="Creating MP3...")
        pdcnt = 0
        pd.show()

        # Setting up the properties of audio files such as bitrate and sampling rate
        cmder = Mp3Cmder(self.mw.getRootPath(), setting)

        # Fixme: Only use bundles shown in the framelist of the main window,
        # i.e. Remove getAllBundles, WYSIWYG!
        # TODO: Thus no need to pass FM but should pass a ref to framelist ui

        for i in range(self.framelist.count()):
            bw = self.framelist.getBundleWidget(i)
            os.makedirs("{root}/{dirname}".format(
                        root=self.mw.getRootPath(), dirname=bw.getDirname()), exist_ok=True)

            cmder.ttsBundleWidget(bw)
            pdcnt += 1
            pd.setValue(pdcnt)
            processCoreEvents()

            cmder.compileBundle(bw, isGstatic=isGstatic)
            pdcnt += 1
            pd.setValue(pdcnt)
            processCoreEvents()

        cmder.mergeDirMp3()
        cmder.createBgmLoop()

        # Fixme: More preciously define the progress out of TTS session
        pdcnt += int(self.framelist.count() / 2)
        pd.setValue(pdcnt)
        processCoreEvents()

        cmder.mixWithBgm()

        self.reject()

    def onSfxClicked(self, idx=None):
        list = self.form.sfxList
        try:
            file = getFile(self.mw, "Add song to BGM Loop",
                        dir=self.mw.pref['sfxdir'], filter="*.mp3")
            assert os.path.isdir(file) != True
            lw, w = QListWidgetItem(), Mp3Widget(file)
            lw.setSizeHint(w.sizeHint())

            row = sum(self.sfxCnt[0:idx+1])
            self.sfxCnt[idx] += 1


            list.insertItem(row, lw)
            list.setItemWidget(lw, w)
        except (IndexError, AssertionError):
            print("Invalid file is selected.")
            pass

    def onBgmClicked(self, idx=None):
        # idx parameter is not in use,
        # but it cannot be removed in order to have the same interface with SFX.
        list = self.form.bgmList
        try:
            file = getFile(self.mw, "Add song to BGM Loop",
                        dir=self.mw.pref['bgmdir'], filter="*.mp3")
            assert os.path.isdir(file) != True
            lw, w = QListWidgetItem(), Mp3Widget(file)
            lw.setSizeHint(w.sizeHint())
            list.addItem(lw)
            list.setItemWidget(lw, w)
        except (IndexError, AssertionError):
            print("Invalid file is selected.")
            pass

    def stopAllAudio(self):
        bgmList = self.form.bgmList
        if bgmList.count() <= 0:
            return

        for i in range(1, bgmList.count()):
            w = bgmList.itemWidget(bgmList.item(i))
            w.forceStop()



    def reject(self):
        self.stopAllAudio()
        self.done(0)
        gui.dialogs.close("Mp3Dialog")