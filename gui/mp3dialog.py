import gui
from gui.qt import *
from gui.utils import rmdir, showCritical, getFile
from gui.customs.groupbtn import GroupButton
from gui.customs.mp3widget import Mp3Widget


def onMp3Dialog(mw):
    gui.dialogs.open("Mp3Dialog", mw)


class Mp3Dialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.eset = mw.entrylist.setting
        self.form = gui.forms.mp3dialog.Ui_Mp3Dialog()
        self.form.setupUi(self)
        self.thread = None
        self.setupButton()
        self.setupSfxList()
        self.setupBgmList()
        self.setupProgress()
        self.show()
        # TODO: Is this a real solution to initialize voice ids?
        # Open Preferences and set up voice id.
        # This is called only the first time audio popup opens
        # and set a voice id if it's None.
        if self.mw.entrylist.isVoiceless():
            gui.dialogs.open("Preferences", mw, tab="TTS")

    def setupSfxList(self):
        sfxList = self.form.sfxList
        groups = [self.eset.tags[key] for key in sorted(self.eset.tags)]
        self.sfxCnt = [1] * len(groups)
        for i, group in enumerate(groups):
            lwi, gb = QListWidgetItem(), GroupButton(self.onSfxClicked, group=group, idx=i)
            lwi.setSizeHint(gb.sizeHint())
            sfxList.addItem(lwi)
            sfxList.setItemWidget(lwi, gb)


    def setupBgmList(self):
        bgmList = self.form.bgmList
        lwi, gb = QListWidgetItem(), GroupButton(self.onBgmClicked, group="BGM")
        lwi.setSizeHint(gb.sizeHint())
        bgmList.addItem(lwi)
        bgmList.setItemWidget(lwi, gb)

    def setupButton(self):
        form = self.form
        form.createBtn.clicked.connect(self.onCreate)
        form.stopBtn.setEnabled(False)
        form.stopBtn.clicked.connect(self.stopThread)

        form.settingBtn.clicked.connect(lambda: gui.dialogs.open("Preferences", self.mw, tab="TTS"))

    def setupProgress(self):
        form = self.form
        form.progressBar.setValue(0)

    def onCreate(self):
        if self.mw.entrylist.count() == 0:
            showCritical("No budles found.", title="Error")
            return
        setting = {}
        setting['repeat'] = self.form.wordSpin.value()
        setting['tts'] = self.mw.setting['tts']
        setting['langMap'] = self.mw.entrylist.setting.langMap

        audDest = os.path.join(self.mw.getProjectPath(), "audio")
        rmdir(audDest)
        setting['dest'] = audDest

        sfxList = self.form.sfxList
        bgmList = self.form.bgmList

        # Check if to download online pronounce data or not
        setting['gstatic'] = self.form.gstaticCheck.isChecked()
        # Check if LRC file needs to be created
        setting['lrc'] = self.form.lrcCheck.isChecked()


        sfxdir = {}
        # Key for Entry's dictionary of QLineEdit
        lineKey = None
        for i in range(sfxList.count()):
            iw = sfxList.itemWidget(sfxList.item(i))
            if isinstance(iw, GroupButton):
                lineKey = self.eset.getKeyByTag(iw.group)
                sfxdir[lineKey] = []
                continue

            sfxdir[lineKey].append({"path": iw.mp3path,
                                  "volume": iw.mp.volume()})
        setting['sfx'] = sfxdir

        bgmloop = []
        for i in range(1, bgmList.count()):
            iw = bgmList.itemWidget(bgmList.item(i))
            bgmloop.append({"path": iw.mp3path,
                            "volume": iw.mp.volume()})
        setting['loop'] = bgmloop

        class Mp3HandlerThread(QThread):
            sig = pyqtSignal(str)

            def __init__(self, mw, handler):
                QThread.__init__(self)
                self.mw = mw
                self.handler = handler

            def run(self):
                self.sig.emit("Setting up aufio files. This takes a few minutes")
                self.handler.setupAudio()
                for i in range(self.mw.entrylist.count()):
                    ew = self.mw.entrylist.getByIndex(i)
                    self.sig.emit("Creating audio file of %s." % ew.atop)
                    os.makedirs(os.path.join(audDest, ew.getDirname()), exist_ok=True)
                    self.handler.runSpeaker(ew)

                self.sig.emit("Mixing with BGM. This takes a few minutes.")
                acapella = sum(self.handler.acapList)
                final = acapella.overlay(self.handler.getBgmLoop(len(acapella)))
                final.export(setting['dest'] + "/Final.mp3")
                self.quit()

        from tools.handler.mp3handler import Mp3Handler
        print("Audio setting: ", setting)
        handler = Mp3Handler(setting)
        self.form.progressBar.setRange(0, self.mw.entrylist.count()+3)

        def onUpdate(msg):
            self.form.pgMsg.setText(msg)
            val = self.form.progressBar.value()
            self.form.progressBar.setValue(val+1)

        self.thread = Mp3HandlerThread(self.mw, handler)
        self.thread.sig.connect(onUpdate)
        self.thread.start()
        self.form.createBtn.setEnabled(False)
        self.form.stopBtn.setEnabled(True)
        self.thread.finished.connect(self.reject)

    def stopThread(self):
        if self.thread:
            self.thread.terminate()
            audDest = os.path.join(self.mw.getProjectPath(), "audio")
            rmdir(audDest)
            self.form.progressBar.reset()
            self.form.pgMsg.setText("")
        self.form.stopBtn.setEnabled(False)
        self.form.createBtn.setEnabled(True)


    def onSfxClicked(self, idx=None):
        sfxList = self.form.sfxList
        try:
            file = getFile(self.mw, "Add song to BGM Loop",
                        dir=self.mw.setting['sfxdir'], filter="*.mp3")
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
            file = getFile(self.mw, "Add song to BGM Loop",
                        dir=self.mw.setting['bgmdir'], filter="*.mp3")
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
        self.form.stopBtn.setEnabled(False)
        self.form.createBtn.setEnabled(True)
        self.form.progressBar.reset()
        self.form.pgMsg.setText("")
        self.stopAllAudio()
        self.done(0)
        gui.dialogs.close("Mp3Dialog", save=True)