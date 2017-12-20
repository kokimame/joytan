import shutil

import gui
from gui.qt import *
from gui.utils import showCritical
from gui.widgets.groupbtn import GroupButton
from gui.widgets.barplayer import BarPlayer


def on_audiodialog(mw):
    gui.dialogs.open("AudioDialog", mw)


class AudioDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.mset = mw.setting
        self.eset = mw.entrylist.setting
        self.form = gui.forms.audiodialog.Ui_AudioDialog()
        self.thread = None
        self.form.setupUi(self)
        self._ui_button()
        self._ui_sfxlist()
        self._ui_bgmlist()
        self._ui_progress()
        self.show()

    def _ui_sfxlist(self):
        sfxs = self.form.sfxList
        keys = [key for key in sorted(self.eset.ttsmap)]
        self._sfx_cnt = [1] * len(keys)
        for i, key in enumerate(keys):
            lwi = QListWidgetItem()
            gb = GroupButton(self.mw, key, self.mset['sfxdir'], idx=i,
                             msg="Add sound effect to %s" % key)
            gb.sig.connect(self._on_new_player)
            lwi.setSizeHint(gb.sizeHint())
            sfxs.addItem(lwi)
            sfxs.setItemWidget(lwi, gb)

    def _ui_bgmlist(self):
        bgms = self.form.bgmList
        lwi = QListWidgetItem()
        gb = GroupButton(self.mw, "BGM", self.mset['bgmdir'],
                         msg="Add song to BGM Loop")
        gb.sig.connect(self._on_new_player)
        lwi.setSizeHint(gb.sizeHint())
        bgms.addItem(lwi)
        bgms.setItemWidget(lwi, gb)

    def _ui_button(self):
        form = self.form
        form.createBtn.clicked.connect(self._on_create)
        form.stopBtn.setEnabled(False)
        form.stopBtn.clicked.connect(self._on_stop_thread)
        form.settingBtn.clicked.connect(
            lambda: gui.dialogs.open("Preferences", self.mw, tab="TTS"))

    def _ui_progress(self):
        form = self.form
        form.progressBar.setValue(0)

    def _on_create(self):
        if self.mw.entrylist.count() == 0:
            showCritical("No entries found in your entry list.", title="Error")
            return

        # Open Preferences and set up voice id.
        # This is called only the first time audio popup opens
        # and set a voice id if it's None.
        if self.eset.is_voiceless():
            showCritical("Please set TTS voice to all section", title="Error")
            gui.dialogs.open("Preferences", self.mw, tab="ATTS")
            return

        setting = {}
        setting['title'] = self.mset['title']
        setting['repeat'] = self.form.wordSpin.value()
        setting['ttsmap'] = self.eset.ttsmap

        destdir = os.path.join(self.mw.basepath(), "audio")
        if os.path.isdir(destdir):
            shutil.rmtree(destdir)
        setting['dest'] = destdir

        sfxs = self.form.sfxList
        bgms = self.form.bgmList

        # Check if LRC file needs to be created
        setting['lrc'] = self.form.lrcCheck.isChecked()
        # Check if row number needs to be read in the output
        setting['idx'] = self.form.idxCheck.isChecked()

        sfxdir = {}
        # Key for Entry's dictionary of QLineEdit
        _key = None
        for i in range(sfxs.count()):
            iw = sfxs.itemWidget(sfxs.item(i))
            if isinstance(iw, GroupButton):
                _key = iw.group
                sfxdir[_key] = []
                continue

            sfxdir[_key].append({"path": iw.mp3path,
                                 "volume": iw.mp.volume()})
        setting['sfx'] = sfxdir

        bgmloop = []
        for i in range(1, bgms.count()):
            iw = bgms.itemWidget(bgms.item(i))
            bgmloop.append({"path": iw.mp3path,
                            "volume": iw.mp.volume()})
        setting['loop'] = bgmloop

        fin_mp3 = os.path.join(setting['dest'], setting['title'] + ".mp3")
        fin_lrc = os.path.join(setting['dest'], setting['title'] + ".lrc")

        class Mp3HandlerThread(QThread):
            prog = pyqtSignal(str)

            def __init__(self, mw, handler):
                QThread.__init__(self)
                self.mw = mw
                self.handler = handler

            def run(self):
                self.prog.emit("Setting up aufio files. This takes a few minutes")
                self.handler.setup_audio()
                for i in range(self.mw.entrylist.count()):
                    ew = self.mw.entrylist.get_entry_at(i)
                    self.prog.emit("Creating audio file of %s." % ew.editors['atop'].text())
                    os.makedirs(os.path.join(destdir, ew.str_index()), exist_ok=True)
                    self.handler.onepass(ew)

                self.prog.emit("Mixing with BGM. This takes a few minutes.")
                acapella = sum(self.handler.acapellas)
                print("Acap")
                if len(setting['loop']) != 0:
                    final = acapella.overlay(self.handler.get_bgmloop(len(acapella)))
                    final.export(fin_mp3)
                else:
                    acapella.export(fin_mp3)

                if setting['lrc']:
                    self.handler.write_lyrics(fin_lrc)

                self.quit()

        from emotan.handler.mp3handler import Mp3Handler
        print("Audio setting: ", setting)
        handler = Mp3Handler(setting)
        self.form.progressBar.setRange(0, self.mw.entrylist.count()+3)

        def _on_progress(msg):
            self.form.pgMsg.setText(msg)
            val = self.form.progressBar.value()
            self.form.progressBar.setValue(val+1)
            
        self.thread = Mp3HandlerThread(self.mw, handler)
        self.thread.prog.connect(_on_progress)
        self.thread.start()
        self.form.createBtn.setEnabled(False)
        self.form.stopBtn.setEnabled(True)
        self.thread.finished.connect(self.reject)

    def _on_stop_thread(self):
        if self.thread:
            self.thread.terminate()
            destdir = os.path.join(self.mw.basepath(), "audio")
            shutil.rmtree(destdir)
            self.form.progressBar.reset()
            self.form.pgMsg.setText("")
        self.form.stopBtn.setEnabled(False)
        self.form.createBtn.setEnabled(True)

    def _on_new_player(self, mp3path, group, idx):
        lwi = QListWidgetItem()
        wig = BarPlayer(mp3path, group, lwi)
        wig.sig.connect(self._on_kill_player)
        lwi.setSizeHint(wig.sizeHint())

        if group == "BGM":
            _list = self.form.bgmList
            _list.addItem(lwi)
        else:
            _list = self.form.sfxList
            row = sum(self._sfx_cnt[0:idx + 1])
            self._sfx_cnt[idx] += 1
            _list.insertItem(row, lwi)

        _list.setItemWidget(lwi, wig)

    def _on_kill_player(self, group, lwi):
        # Update counter of SFX
        def _re_sfxcounter(i):
            sum = 0
            for j, cnt in enumerate(self._sfx_cnt):
                sum += cnt
                if sum > i:
                    self._sfx_cnt[j] -= 1
                    break

        if group == "BGM":
            _list = self.form.bgmList
        else:
            _list = self.form.sfxList

        for i in range(_list.count()):
            if lwi == _list.item(i):
                _list.takeItem(i)
                if group != "BGM":
                    _re_sfxcounter(i)

    def stop_all_audio(self):
        bgms = self.form.bgmList
        if bgms.count() <= 0:
            return

        for i in range(1, bgms.count()):
            w = bgms.itemWidget(bgms.item(i))
            w.force_stop()

    def reject(self):
        self.form.stopBtn.setEnabled(False)
        self.form.createBtn.setEnabled(True)
        self.form.progressBar.reset()
        self.form.pgMsg.setText("")
        self.stop_all_audio()
        self.done(0)
        gui.dialogs.close("AudioDialog", save=True)
