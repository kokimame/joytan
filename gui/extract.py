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
        self.form = gui.forms.extractdialog.Ui_ExtractDialog()
        self.form.setupUi(self)

        _list = self.form.keyList
        for _key in self.mw.entrylist.setting._keys():
            check = QCheckBox(_key)
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
        words = self._extract()

        _keys = []
        _list = self.form.keyList
        for i in range(_list.count()):
            ch = _list.itemWidget(_list.item(i))
            if ch.isChecked():
                _keys.append(ch.text())

        if len(_keys) == 0:
            showCritical("No destination selected", title="Error")
            return

        if self.form.overCheck.isChecked():
            for i in range(len(words)):
                new_item = dict((_key, words[i]) for _key in _keys)
                # Existing entry to be overwritten
                if i + 1 <= self.mw.entrylist.count():
                    ew = self.mw.entrylist.get_entry_at(i)
                    ew.update_editor(new_item)
                else:
                    ew = self.mw.entrylist.add_entry('', self.mw.mode)
                    ew.update_editor(new_item)
        else:
            for word in words:
                new_item = dict((_key, word) for _key in _keys)
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
