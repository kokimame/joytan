from gui.qt import *
import gui
import gui.utils as utils
from tools.cmder.mp3cmder import mp3Duration, getMp3Info


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
    def __init__(self, mp3path, groupIdx, delTrigger, lwi):
        super(Mp3Widget, self).__init__()
        self.mp = MediaPlayer(self)
        self.mp3path = mp3path
        self.gidx = groupIdx
        self.delTrigger = delTrigger
        self.lwi = lwi      # ListWidgetItem that contains this widget
        self.filename = utils.getFileNameFromPath(mp3path)
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



class Mp3Dialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.form = gui.forms.mp3dialog.Ui_Mp3Dialog()
        self.form.setupUi(self)
        self.setupButton()
        self.setupSfxList()
        self.setupBgmList()
        self.setupProgress()
        self.show()
        # TODO: Is this a real solution to initialize voice ids?
        # Open Preferences and set up voice id.
        # This is called only the first time audio popup opens
        # and set a voice id if it's None.
        gui.dialogs.open("Preferences", mw, tab="TTS")

    def setupSfxList(self):
        sfxList = self.form.sfxList
        sfxList.setStyleSheet("""
                              QListWidget::item { border-bottom: 1px solid black; }
                              QListWidget::item { background-color: rgb(200,200,200); }
                              """)
        groups = ['word', 'definition', 'example']
        self.sfxCnt = [1] * len(groups)
        for i, group in enumerate(groups):
            lwi, gb = QListWidgetItem(), GroupButton(self.onSfxClicked, group=group, idx=i)
            lwi.setSizeHint(gb.sizeHint())
            sfxList.addItem(lwi)
            sfxList.setItemWidget(lwi, gb)


    def setupBgmList(self):
        bgmList = self.form.bgmList
        bgmList.setStyleSheet("""
                              QListWidget::item { border-bottom: 1px solid black; }
                              QListWidget::item { background-color: rgb(200,200,200); }
                              """)
        lwi, gb = QListWidgetItem(), GroupButton(self.onBgmClicked, group="BGM")
        lwi.setSizeHint(gb.sizeHint())
        bgmList.addItem(lwi)
        bgmList.setItemWidget(lwi, gb)

    def setupButton(self):
        form = self.form
        form.createBtn.clicked.connect(self.onCreate)
        form.cancelBtn.clicked.connect(self.reject)

        form.settingBtn.clicked.connect(lambda: gui.dialogs.open("Preferences", self.mw, tab="TTS"))

    def setupProgress(self):
        form = self.form
        form.progressBar.setValue(0)

    def onCreate(self):
        if self.mw.framelist.count() == 0:
            utils.showCritical("No budles found.", title="Error")
            return
        setting = {}
        setting['repeat'] = self.form.wordSpin.value()
        setting['tts'] = self.mw.pref['tts']
        setting['langMap'] = self.mw.framelist.setting.langMap

        from gui.utils import rmdir
        audDest = os.path.join(self.mw.getRootPath(), "audio")
        rmdir(audDest)
        setting['dest'] = audDest

        sfxList = self.form.sfxList
        bgmList = self.form.bgmList
        # Check if nice pronunciation is needs to be downloaded
        isGstatic = self.form.gstaticCheck.isChecked()
        # Check if LRC file needs to be created
        setting['lrc'] = self.form.lrcCheck.isChecked()

        sfxdir = {}
        group = None
        for i in range(sfxList.count()):
            iw = sfxList.itemWidget(sfxList.item(i))
            if isinstance(iw, GroupButton):
                group = iw.group
                sfxdir[group] = []
                continue

            sfxdir[group].append({"path": iw.mp3path,
                                  "filename": iw.filename,
                                  "duration": iw.duration,
                                  "sampling": iw.fskhz,
                                  "bitrate": iw.bitkbs,
                                  "volume": iw.mp.volume()})
        setting['sfx'] = sfxdir

        bgmloop = []
        for i in range(1, bgmList.count()):
            iw = bgmList.itemWidget(bgmList.item(i))
            bgmloop.append({"path": iw.mp3path,
                            "filename": iw.filename,
                            "duration": iw.duration,
                            "sampling": iw.fskhz,
                            "bitrate": iw.bitkbs,
                            "volume": iw.mp.volume()})
        setting['loop'] = bgmloop


        class Mp3Thread(QThread):
            sig = pyqtSignal(str)
            def __init__(self, mw, cmder):
                QThread.__init__(self)
                self.mw = mw
                self.cmder = cmder

            def run(self):
                # Setting up the properties of audio files such as bitrate and sampling rate
                self.sig.emit("Setting up aufio files. This takes a few minues")
                self.cmder.setupAudio()

                for i in range(self.mw.framelist.count()):
                    bw = self.mw.framelist.getBundleWidget(i)
                    self.sig.emit("Creating audio file of %s." % bw.name)
                    os.makedirs(os.path.join(audDest, bw.getDirname()), exist_ok=True)
                    self.cmder.dictateContents(bw)
                    self.cmder.compileBundle(bw, isGstatic=isGstatic)

                self.cmder.mergeMp3s()
                self.cmder.createBgmLoop()
                self.sig.emit("Mixing with BGM. This takes a few minutes.")
                self.cmder.mixWithBgm()

                self.save(self.cmder.finalMp3)
                self.quit()

            def save(self, file):
                pref = self.mw.pref
                output = os.path.join(pref['workspace'], pref['title'] + '-audio.mp3')
                from shutil import copyfile
                copyfile(file, output)

        from tools.cmder.mp3cmder import Mp3Cmder
        cmder = Mp3Cmder(setting)
        self.form.progressBar.setRange(0, self.mw.framelist.count()+2)

        def onUpdate(msg):
            self.form.pgMsg.setText(msg)
            val = self.form.progressBar.value()
            self.form.progressBar.setValue(val+1)

        self.thread = Mp3Thread(self.mw, cmder)
        self.thread.sig.connect(onUpdate)
        self.thread.start()
        self.thread.finished.connect(self.reject)

    def onSfxClicked(self, idx=None):
        sfxList = self.form.sfxList
        try:
            file = utils.getFile(self.mw, "Add song to BGM Loop",
                        dir=self.mw.pref['sfxdir'], filter="*.mp3")
            assert os.path.isdir(file) != True
            lwi = QListWidgetItem()
            w = Mp3Widget(file, idx, self.onDeleteSfx, lwi)
            lwi.setSizeHint(w.sizeHint())

            row = sum(self.sfxCnt[0:idx+1])
            self.sfxCnt[idx] += 1


            sfxList.insertItem(row, lwi)
            sfxList.setItemWidget(lwi, w)
        except (IndexError, AssertionError, TypeError):
            print("Error: Invalid file is selected.")
            pass

    def onBgmClicked(self, idx=None):
        # idx parameter is not in use,
        # but it cannot be removed in order to have the same interface with SFX.
        bgmList = self.form.bgmList
        try:
            file = utils.getFile(self.mw, "Add song to BGM Loop",
                        dir=self.mw.pref['bgmdir'], filter="*.mp3")
            assert os.path.isdir(file) != True
            lwi = QListWidgetItem()
            w = Mp3Widget(file, idx, self.onDeleteBgm, lwi)
            lwi.setSizeHint(w.sizeHint())
            bgmList.addItem(lwi)
            bgmList.setItemWidget(lwi, w)
        except (IndexError, AssertionError, TypeError):
            print("Error: Invalid file is selected.")
            pass

    def onDeleteSfx(self, lwi):
        sfxList = self.form.sfxList
        for i in range(sfxList.count()):
            if lwi == sfxList.item(i):
                sfxList.takeItem(i)
                # Update counter for sfx
                sum = 0
                for j, cnt in enumerate(self.sfxCnt):
                    sum += cnt
                    if sum > i:
                        self.sfxCnt[j] -= 1
                        break

                break


    def onDeleteBgm(self, lwi):
        bgmList = self.form.bgmList
        for i in range(bgmList.count()):
            if lwi == bgmList.item(i):
                bgmList.takeItem(i)
                break

    def stopAllAudio(self):
        bgmList = self.form.bgmList
        if bgmList.count() <= 0:
            return

        for i in range(1, bgmList.count()):
            w = bgmList.itemWidget(bgmList.item(i))
            w.forceStop()

    def reject(self):
        self.form.progressBar.reset()
        self.form.pgMsg.setText("")
        self.stopAllAudio()
        self.done(0)
        gui.dialogs.close("Mp3Dialog", save=True)