import shutil

import gui
from gui.qt import *
from gui.utils import showCritical, getFiles
from gui.widgets.flowitem import FlowItem, Mp3Object, EwkeyObject, Rest


def on_audiodialog(mw):
    gui.dialogs.open("AudioDialog", mw)


class AudioDialog(QDialog):

    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.thread = None
        self.form = gui.forms.audiodialog.Ui_AudioDialog()
        self.form.setupUi(self)

        self.list_lookup = {
            'flow': dict(
                ui=self.form.flowList,
                dir_type='sfxdir',
                dir_msg='Select sound effect',
            ),
            'bgm': dict(
                ui=self.form.bgmList,
                dir_type='bgmdir',
                dir_msg='Select BGM',
            )
        }
        self._ui_button()
        self._ui_progress()
        self._ui_add_flow()
        self._ui_add_bgm()

        self.show()

    def _ui_button(self):
        form = self.form
        form.createBtn.clicked.connect(self._on_create)
        form.stopBtn.setEnabled(False)
        form.stopBtn.clicked.connect(self._on_stop_thread)
        form.settingBtn.clicked.connect(
            lambda: gui.dialogs.open("Preferences", self.mw, back_to=self, tab="TTS"))

    def _ui_progress(self):
        form = self.form
        form.progressBar.setValue(0)

    def _ui_add_flow(self):
        fadd = self.form.flowAdd
        fadd.clicked.connect(self._flow_tool)
        fadd.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        fadd.setArrowType(Qt.DownArrow)

        for ewkey in self.mw.entrylist.get_config('ewkeys'):
            self._add_item(self.list_lookup['flow'], ewkey)

    def _ui_add_bgm(self):
        badd = self.form.bgmAdd
        badd.clicked.connect(self._bgm_tool)
        badd.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        badd.setArrowType(Qt.DownArrow)

    def _flow_tool(self):
        m = QMenu(self.mw)
        a = m.addAction("Add Sound effect")
        a.triggered.connect(lambda: self._add_item(self.list_lookup['flow'], 'MP3'))
        a = m.addAction("Add Rest")
        a.triggered.connect(lambda: self._add_item(self.list_lookup['flow'], 'REST'))
        for ewkey in self.mw.entrylist.get_config('ewkeys'):
            a = m.addAction("Add %s" % ewkey)
            a.triggered.connect(lambda ignore, type=ewkey:
                                self._add_item(self.list_lookup['flow'], type))
        m.exec_(QCursor.pos())

    def _bgm_tool(self):
        m = QMenu(self.mw)
        a = m.addAction("Add Song")
        a.triggered.connect(lambda: self._add_item(self.list_lookup['bgm'], 'MP3'))
        a = m.addAction("Add Silence")
        a.triggered.connect(lambda: self._add_item(self.list_lookup['bgm'], 'REST'))
        m.exec_(QCursor.pos())

    def _add_item(self, lookup, item_type):
        # Type may spawn multiple flow item
        if item_type == 'MP3':
            try:
                files = getFiles(self.mw, lookup['dir_msg'],
                                 dir=self.mw.config[lookup['dir_type']], filter="*.mp3")
            except:
                return

            for file in files:
                lwi = QListWidgetItem()
                fi = Mp3Object(file)
                lwi.setSizeHint(fi.sizeHint())
                fi.delete.connect(lambda base=lookup['ui'], item=lwi: self._remove_item(base, item))
                lookup['ui'].addItem(lwi)
                lookup['ui'].setItemWidget(lwi, fi)
            return
        # ======================
        # Types for single flow item
        elif item_type == 'REST':
            lwi = QListWidgetItem()
            fi = Rest()
        else:
            assert item_type in self.mw.entrylist.get_config('ewkeys')
            lwi = QListWidgetItem()
            fi = EwkeyObject(item_type)

        lwi.setSizeHint(fi.sizeHint())
        fi.delete.connect(lambda base=lookup['ui'], item=lwi: self._remove_item(base, item))
        lookup['ui'].addItem(lwi)
        lookup['ui'].setItemWidget(lwi, fi)

    def _remove_item(self, _list, lwi):
        for i in range(_list.count()):
            if lwi == _list.item(i):
                _list.takeItem(i)

    def _on_create(self):
        el = self.mw.entrylist
        if el.count() == 0:
            showCritical("No entries found in your entry list.")
            return

        # Open TTS setting dialog if TTS is not allocated to
        # all of EntryWidget's text editor
        if el.get_config('voiceless'):
            showCritical("Please set TTS voice to all section")
            gui.dialogs.open("Preferences", self.mw, tab="ATTS")
            return

        setting = {}
        setting['title'] = self.mw.config['title']
        setting['ttsmap'] = el.get_config('ttsmap')

        destdir = os.path.join(self.mw.projectbase(), "audio")
        if os.path.isdir(destdir):
            shutil.rmtree(destdir)
        setting['dest'] = destdir

        # Check if LRC file needs to be created
        setting['lrc'] = self.form.lrcCheck.isChecked()
        # Check if index needs to be read in the output
        setting['idx'] = self.form.idxCheck.isChecked()

        _list = self.form.flowList
        flow = []
        for i in range(_list.count()):
            fi = _list.itemWidget(_list.item(i))
            assert isinstance(fi, FlowItem)
            if isinstance(fi, Mp3Object):
                flow.append({"type": "MP3",
                                 "path": fi.mp3path,
                                 "volume": fi.mp.volume()})
            elif isinstance(fi, Rest):
                flow.append({"type": "REST",
                                 "duration": fi.get_duration()})
            elif isinstance(fi, EwkeyObject):
                flow.append({"type": fi.ewkey})
        setting['flow'] = flow

        _list = self.form.bgmList
        loop = []
        for i in range(_list.count()):
            fi = _list.itemWidget(_list.item(i))
            assert isinstance(fi, FlowItem)
            if isinstance(fi, Mp3Object):
                loop.append({"type": "MP3",
                                "path": fi.mp3path,
                                "volume": fi.mp.volume()})
            elif isinstance(fi, Rest):
                loop.append({"type": "REST",
                                "duration": fi.get_duration()})
        setting['loop'] = loop

        finalpath = os.path.join(setting['dest'], setting['title'])

        class Mp3HandlerThread(QThread):
            prog = pyqtSignal(str)

            def __init__(self, mw, handler):
                QThread.__init__(self)
                self.mw = mw
                self.handler = handler

            def run(self):
                self.prog.emit("Setting up aufio files. This may take a few minutes")
                self.handler.setup_audio()
                for i in range(el.count()):
                    ew = el.get_entry_at(i)
                    self.prog.emit("Creating audio file of %s." % ew.editors['atop'].text())
                    os.makedirs(os.path.join(destdir, ew.str_index()), exist_ok=True)
                    self.handler.onepass(ew)

                self.prog.emit("Mixing with BGM. This may take a few minutes.")
                acapella = sum(self.handler.acapellas)
                if len(setting['loop']) != 0:
                    finalmp3 = acapella.overlay(self.handler.get_bgmloop(len(acapella)))
                    finalmp3.export(finalpath + ".mp3")
                else:
                    acapella.export(finalpath + ".mp3")

                if setting['lrc']:
                    self.handler.write_lyrics(finalpath + ".lrc")

                self.quit()

        from joytan.handler.mp3handler import Mp3Handler
        handler = Mp3Handler(setting)
        self.form.progressBar.setRange(0, el.count()+3)

        def _on_progress(msg):
            self.form.pgMsg.setText(msg)
            val = self.form.progressBar.value()
            self.form.progressBar.setValue(val+1)
            
        self.thread = Mp3HandlerThread(self.mw, handler)
        self.thread.prog.connect(_on_progress)
        self.thread.start()
        self.form.createBtn.setEnabled(False)
        self.form.stopBtn.setEnabled(True)
        # self.thread.finished.connect(self.reject)

    def _on_stop_thread(self):
        if self.thread:
            self.thread.terminate()
            destdir = os.path.join(self.mw.projectbase(), "audio")
            shutil.rmtree(destdir)
            self.form.progressBar.reset()
            self.form.pgMsg.setText("")
        self.form.stopBtn.setEnabled(False)
        self.form.createBtn.setEnabled(True)

    def stop_all_audio(self):
        for _list in [self.form.flowList, self.form.bgmList]:
            for i in range(_list.count()):
                iw = _list.itemWidget(_list.item(i))
                if isinstance(iw, Mp3Object):
                    iw.force_stop()

    def reject(self):
        self.form.stopBtn.setEnabled(False)
        self.form.createBtn.setEnabled(True)
        self.form.progressBar.reset()
        self.form.pgMsg.setText("")
        self.stop_all_audio()
        self.done(0)
        gui.dialogs.close("AudioDialog")
