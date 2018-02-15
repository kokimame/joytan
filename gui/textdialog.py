# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html
import re

import gui
from gui.qt import *
from gui.widgets.panellane import *
from gui.utils import path2filename, showCritical, getCompleted, getFile, ConfirmDialog
from joytan.frozen import FROZEN_TEXTBOOK

def on_textdialog(mw):
    gui.dialogs.open("TextDialog", mw)


class BookDesign:
    """
    Represents a design of textbook, parsing Jinja2 template of HTML to detect
    the maximum number of images for a given Entry. The class provides an actual
    template object from Jinja2 Environment in the process of creating a textbook.
    """

    RE_MAXIMG = re.compile(r'<!---maximg:(\d*)--->')

    def __init__(self, path=None):
        # If the app is bundled app and design is not specified,
        # look for the default design, which was distributed with the app
        if not path and getattr(sys, 'frozen', False):
            if os.path.exists(FROZEN_TEXTBOOK):
                self.path = FROZEN_TEXTBOOK
        else:
            self.path = path

        if self.path:
            self.name = path2filename(self.path)
            self.maximg = self._parse_design()
            self.info = "%s / image:%d" % (self.name, self.maximg)

    def _parse_design(self):
        with open(self.path, 'r') as f:
            res = self.RE_MAXIMG.search(f.readline())
            assert res
        return int(res.group(1))

    def get_template(self):
        from jinja2 import Environment, FileSystemLoader
        directory, filename = os.path.split(self.path)
        env = Environment(loader=FileSystemLoader(directory))
        return env.get_template(filename)


class TextDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        # Thread pool for downloading images
        self.pool = None
        if os.path.isdir(self._destdir()):
            import shutil
            shutil.rmtree(self._destdir())
        os.makedirs(self._destdir())
        self.form = gui.forms.textdialog.Ui_TextDialog()
        self.form.setupUi(self)
        self.form.startBtn.clicked.connect(self._on_create)
        self._ui()

        # Try to find default book design
        try:
            self.book = BookDesign()
            self._activate_imglist()
            self.form.designLbl.setText(self.book.info)
        except:
            pass

        self.show()

    def _ui(self):
        # Use QLineEdit as QLabel with disabling selection
        label = self.form.designLbl
        label.selectionChanged.connect(label.deselect)
        self.form.designBtn.clicked.connect(self._on_design_select)
        self.form.dlAllBtn.clicked.connect(self._autodownload)
        self.form.clearAllBtn.clicked.connect(self._clear_all_images)
        self.form.stopBtn.clicked.connect(self._on_stop)

    def _autodownload(self):
        if not self.book:
            showCritical("Please select textbook design. If you don't have any design file,"
                         " you can download various designs from our website.")
            return

        for i in range(self.mw.entrylist.count()):
            lane = self._get_lane(i)
            lane.wait_all()

        # The actual class to be run in the following pool
        class Worker(QRunnable):
            def __init__(self, lane):
                QRunnable.__init__(self)
                self.lane = lane

            def run(self):
                self.lane.start_working()
                self.lane.thread.run()

        self.pool = QThreadPool()
        # Only 4 threads working at the same time
        self.pool.setMaxThreadCount(4)

        for i in range(self.mw.entrylist.count()):
            lane = self._get_lane(i)
            waiting = lane.is_waiting()
            if waiting:
                lane.thread.set_total(waiting)
                self.pool.start(Worker(lane))

    def _activate_imglist(self):
        assert self.book.path, "Book design is not defined"

        _list = self.form.imgList
        for i, ew in enumerate(self.mw.entrylist.get_entry_all()):
            if ew['atop'] == '':
                # if ew is empty, ignore it
                continue
            group = ew['atop']
            destdir = os.path.join(self._destdir(), ew.str_index())
            lwi1 = QListWidgetItem()
            lwi2 = QListWidgetItem()
            pb = QPushButton('+ Download %s' % group)
            pb.setStyleSheet("Text-align: left")
            ip = PanelLane(group, self.form.followEdit.text(), destdir, self.book.maximg)
            pb.clicked.connect(ip.on_download)
            lwi1.setSizeHint(pb.sizeHint())
            self.form.followEdit.textChanged.connect(ip.on_update_following)
            lwi2.setSizeHint(ip.size())

            _list.addItem(lwi1)
            _list.setItemWidget(lwi1, pb)
            _list.addItem(lwi2)
            _list.setItemWidget(lwi2, ip)

    def _on_design_select(self):
        try:
            path = getFile(self, "Select book design", dir=self.mw.projectbase(),
                           filter="Jinja template HTML file (*.html)")
        except:
            return
        try:
            self.book = BookDesign(path)
            self._clear_imglist()
            self._activate_imglist()
            self.form.designLbl.setText(self.book.info)
        except AssertionError:
            showCritical("Invalid book design (Image number not found)")

    @pyqtSlot()
    def _clear_all_images(self):
        for i in range(self.mw.entrylist.count()):
            lane = self._get_lane(i)
            lane.clear_all()

    def _clear_imglist(self):
        for _ in range(self.form.imgList.count()):
            self.form.imgList.takeItem(0)

    def _get_lane(self, i):
        _list = self.form.imgList
        return _list.itemWidget(_list.item(2 * i + 1))

    def _on_create(self):
        if not self.book.path:
            showCritical("Please select textbook design. If you don't have any design file,"
                         " you can download various designs from our website.")
            return
        datas = []
        for i, ew in enumerate(self.mw.entrylist.get_entry_all()):
            data = ew.data()
            data['idx'] = i + 1
            panel = self._get_lane(i)
            if panel:
                for j, tup in enumerate(panel.imglist):
                    data['img-%d' % (j + 1)] = tup[0]
                    data['cite-%d' % (j + 1)] = tup[1]
            datas.append(data)

        template = self.book.get_template()
        rendered_temp = template.render(entries=datas)

        with open(self._destdir() + ".html", 'w', encoding='utf-8') as f:
            f.write(rendered_temp)

        self._completed(self._destdir() + ".html")

    def _on_stop(self):
        if self.pool:
            self.pool.clear()
        for i in range(self.mw.entrylist.count()):
            lane = self._get_lane(i)
            if lane.is_waiting:
                lane.force_finish()

    def _destdir(self):
        return os.path.join(self.mw.projectbase(), "textbook")

    def _completed(self, path):
        getCompleted(path, hint="\nOpen the file with your browser.")

    def reject(self):
        def close_dialog():
            self.done(0)
            gui.dialogs.close("TextDialog")

        # d = ConfirmDialog(self, "With version %s, " % gui.app_version +
        #                           "all downloaded images will be lost after closing this dialog.\n"
        #                           "Sorry for the inconvenience.")
        # d.setWindowModality(Qt.WindowModal)
        # d.accepted.connect(close_dialog)
        # d.exec_()
        close_dialog()
