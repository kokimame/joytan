import gui
from gui.qt import *
from gui.widgets.groupbtn import GroupButton
from gui.widgets.imgpanel import *
from gui.utils import path2filename


def on_textdialog(mw):
    gui.dialogs.open("TextDialog", mw)


# Not in use
class TxtThread(QThread):
    def __init__(self, mw, dest):
        QThread.__init__(self)
        self.mw = mw
        self.dest = dest

    def run(self):
        ftxt = open("{dest}/{title}.txt".format(dest=self.dest, title=self.mw.setting['title']), 'w')
        for i in range(self.mw.entrylist.count()):
            ew = self.mw.entrylist.get_entry_at(i)
            ftxt.write("{index}. {name}\n".format(
                index=ew.row+1, name=ew.editors['atop'].text()))
            for j in range(0, ew.lv1):
                if ew.editors['def-%d' % (j + 1)].text() != '':
                    ftxt.write(ew.editors['def-%d' % (j + 1)].text() + '\n')
                for k in range(0, ew.lv2):
                    if ew.editors['ex-%d-%d' % (j + 1, k + 1)].text() != '':
                        ftxt.write('\t' + ew.editors['ex-%d-%d' % (j + 1, k + 1)].text() + '\n')
            ftxt.write('\n')
        ftxt.close()


# Not in use
class HtmlThread(QThread):
    def __init__(self, mw, dest):
        QThread.__init__(self)
        self.mw = mw
        self.dest = dest

    def run(self):
        datas = [ew.data() for ew in self.mw.entrylist.get_entry_all()]

        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader('templates/html'))
        temp = env.get_template('words.html')
        rendered_temp = temp.render(entries=datas)

        with open('{dest}/{title}.html'.format(dest=self.dest, title=self.mw.setting['title']), 'w') as f:
            f.write(rendered_temp)


class BookDesign:
    def __init__(self, path):
        self.path = path
        self.name = path2filename(path)
        self.maximg = self._parse_maximg(path)
        self.info = "%s / image:%d" % (self.name, self.maximg)

    def _parse_maximg(self, path):
        import re

        with open(path, 'r') as f:
            vimg = re.compile(r'<!---maximg:(\d*)--->')
            res = vimg.search(f.readline())
            assert res

        return int(res.group(1))


class TextDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.book = None
        self.destdir = os.path.join(mw.basepath(), "text")
        self.form = gui.forms.textdialog.Ui_TextDialog()
        self.form.setupUi(self)
        self.form.startBtn.clicked.connect(self._on_create)
        self._ui()
        self.show()

    def _ui(self):
        dlbl = self.form.designLbl
        dlbl.selectionChanged.connect(dlbl.deselect)
        self.form.designBtn.clicked.connect(self._on_design_select)

    def _activate_imglist(self):
        assert self.book, "Book design is not defined"

        _list = self.form.imgList
        for i, ew in enumerate(self.mw.entrylist.get_entry_all()):
            group = ew.editors['atop'].text()
            index = 2 * i + 1
            destdir = os.path.join(self.destdir, ew.str_index())
            if group == '':
                # TODO: Change 'pass' to 'continue' on commit
                pass
            lwi1 = QListWidgetItem()
            gb = GroupButton(self.mw, group, filter="Images (*.jpg *.jpeg *.png)",
                             idx=index, dir=self.mw.basepath(), msg="Select an Image")
            gb.sig.connect(self._on_image_upload)
            lwi1.setSizeHint(gb.sizeHint())
            lwi2, ip = QListWidgetItem(), ImagePanel(group, destdir, self.book.maximg)
            lwi2.setSizeHint(ip.size())

            _list.addItem(lwi1)
            _list.setItemWidget(lwi1, gb)
            _list.addItem(lwi2)
            _list.setItemWidget(lwi2, ip)

    def _on_image_upload(self, imgpath, group, idx):
        _list = self.form.imgList
        panel = _list.itemWidget(_list.item(idx))

        pixmap = QPixmap(imgpath).scaled(128, 128)
        img = QLabel()
        img.setPixmap(pixmap)
        lwi = QListWidgetItem()
        lwi.setSizeHint(img.sizeHint())
        # Insert item in front of DL button
        panel.insertItem(panel.count() - 1, lwi)
        panel.setItemWidget(lwi, img)
        panel.images.append(imgpath)

    def _on_design_select(self):
        from gui.utils import getFile, path2filename
        path = getFile(self, "Select book design", dir=self.mw.basepath(),
                       filter="Jinja template HTML file (*.html)")
        if path:
            try:
                bd = BookDesign(path)
                self.book = bd
                self._activate_imglist()
                self.form.designLbl.setText(bd.info)
            except Exception as e:
                print("Invalid book design", e)



    def _get_panel(self, i):
        form = self.form
        return form.imgList.itemWidget(form.imgList.item(2 * i + 1))

    def _on_create(self):
        datas = []
        for i, ew in enumerate(self.mw.entrylist.get_entry_all()):
            data = ew.data()
            panel = self._get_panel(i)
            for j, img in enumerate(panel.images):
                data['img-%d' % (j + 1)] = img
            datas.append(data)

        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader('templates/html'))
        temp = env.get_template('words.html')
        rendered_temp = temp.render(entries=datas)

        with open('{dest}.html'.format(dest=self.destdir), 'w', encoding='utf-8') as f:
            f.write(rendered_temp)

    def reject(self):
        self.done(0)
        gui.dialogs.close("TextDialog", save=True)
