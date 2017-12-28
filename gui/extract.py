import re

import gui
from gui.qt import *
import emotan.extractor as extractor
from gui.utils import getFile, path2filename, showCritical


def on_extract(mw):
    gui.dialogs.open("ExtractDialog", mw)


class ExtractDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.path = None
        self._ui()
        self.show()

    def _ui(self):
        self.form = gui.forms.extract.Ui_ExtractDialog()
        self.form.setupUi(self)

        _list = self.form.keyList
        for ewkey in self.mw.entrylist.setting.ewkeys():
            check = QCheckBox(ewkey)
            lwi = QListWidgetItem()
            lwi.setSizeHint(check.sizeHint())
            _list.addItem(lwi)
            _list.setItemWidget(lwi, check)

        self.form.fileBtn.clicked.connect(self._on_file_select)
        self.form.okBtn.clicked.connect(self._on_ok)

    def _extract(self):
        # Various Extractor will be available for a lot of file formats
        # For now, we only _extract from a file with one word in each line

        # Extractor
        exttr = None
        for e in extractor.Extractors:
            for vft in re.findall("[( ]?\*\.(.+?)[) ]", e[0]):
                # If valid file file is chosen
                if self.path.endswith("." + vft):
                    exttr = e[1]
                    break
        if not exttr:
            print("Error: Cannot find proper file extractor.")
            return

        return exttr(self.path).run()

    def _on_ok(self):
        if not self.path:
            showCritical("No file to extract selected.", title="Error")

        ewkeys = []
        _list = self.form.keyList
        for i in range(_list.count()):
            ch = _list.itemWidget(_list.item(i))
            if ch.isChecked():
                ewkeys.append(ch.text())

        if len(ewkeys) == 0:
            showCritical("No destination selected.", title="Error")
            return

        words = self._extract()

        if self.form.overCheck.isChecked():
            for i in range(len(words)):
                new_item = dict((ewkey, words[i]) for ewkey in ewkeys)
                # Existing entry to be overwritten
                if i + 1 <= self.mw.entrylist.count():
                    ew = self.mw.entrylist.get_entry_at(i)
                    ew.update_editor(new_item)
                else:
                    ew = self.mw.entrylist.add_entry('', self.mw.mode)
                    ew.update_editor(new_item)
        else:
            for word in words:
                new_item = dict((ewkey, word) for ewkey in ewkeys)
                ew = self.mw.entrylist.add_entry('', self.mw.mode)
                ew.update_editor(new_item)

        self.reject(update=True)

    def _on_file_select(self):
        filter = ";;".join([x[0] for x in extractor.Extractors])
        try:
            file = getFile(self.mw, "Extract Words from File",
                             dir=self.mw.setting['worddir'], filter=filter)
            self.path = file
            self.form.nameLbl.setText(path2filename(file))
        except:
            pass

    def reject(self, update=False):
        if update:
            self.mw.entrylist.update_all()
        self.done(0)
        gui.dialogs.close("ExtractDialog")
