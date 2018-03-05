# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html

import re
import requests
from bs4 import BeautifulSoup

import gui
from gui.qt import *
from gui.utils import showCritical, showWarning, path2filename


def on_memrise(mw):
    gui.dialogs.open("MemriseDialog", mw)

class MemriseDialog(QDialog):
    """

    """
    URL_FORMAT = re.compile(
        r'https://www.memrise.com/course/([0-9]*)/(.*)/([0-9]+)(/?)'
    )

    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.form = gui.forms.memrise.Ui_MemriseDialog()
        self.form.setupUi(self)

        self._ui_button()
        self._ui_reset()

        self.show()

    def _ui_button(self):
        self.form.dlBtn.clicked.connect(self._on_download)
        self.form.stopBtn.clicked.connect(self._on_stop)

    def _ui_reset(self):
        self.form.dlBtn.setEnabled(True)
        self.form.stopBtn.setEnabled(False)
        self.form.progressBar.reset()
        self.form.pgMsg.setText("")

    def _on_download(self):
        url = self.form.urlEdit.text()
        if not self.URL_FORMAT.match(url):
            showCritical("Wrong URL format is detected.\nPlease choose other URL.")
            return

        self.thread = MemriseThread(url)
        self.thread.logger.connect(showCritical)
        self.thread.bar_size.connect(self._set_bar_size)
        self.thread.prog.connect(self._on_progress)
        self.thread.finished.connect(self._completed)
        self.thread.start()
        self.form.dlBtn.setEnabled(False)
        self.form.stopBtn.setEnabled(True)

    def _on_progress(self, atop, items):
        ew = self.mw.entrylist.add_entry(atop=atop)
        ew.update_editor(items)

        self.form.pgMsg.setText("Download word #%d" % (ew.row + 1))
        val = self.form.progressBar.value()
        self.form.progressBar.setValue(val + 1)

    def _set_bar_size(self, size):
        self.form.progressBar.setRange(0, size)

    def _on_stop(self):
        if isinstance(self.thread, MemriseThread):
            self.thread.quit()
        self._ui_reset()
        self.mw.entrylist.update_all()

    def _completed(self):
        self._ui_reset()
        self.mw.entrylist.update_all()
        self.reject()

    def reject(self):
        self._on_stop()
        self.done(0)
        gui.dialogs.close("MemriseDialog")


class MemriseThread(QThread):

    logger = pyqtSignal(str)
    bar_size = pyqtSignal(int)
    prog = pyqtSignal(str, dict)

    def __init__(self, url):
        QThread.__init__(self)
        self.url = url

    def run(self):
        try:
            r = requests.get(self.url)
        except Exception as e:
            self.logger.emit(e)
            return

        soup = BeautifulSoup(r.content, "html.parser")
        things = soup.find_all('div', attrs={'class': 'thing text-text'})

        try:
            assert len(things) != 0
        except:
            self.logger.emit("No entries found in the Memrise level")
            return

        self.bar_size.emit(len(things))

        try:
            for t in things:
                atop = t.find(
                    'div', attrs={'class': 'col_a col text'}
                ).text.strip()
                items = {
                    'def-1': t.find(
                        'div', attrs={'class': 'col_b col text'}
                    ).text.strip()
                }
                self.prog.emit(atop, items)
        except:
            pass