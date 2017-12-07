import gui
from gui.qt import *
from gui.customs.groupbtn import GroupButton
from gui.customs.imgpanel import *

def onTextDialog(mw):
    gui.dialogs.open("TextDialog", mw)

class TxtThread(QThread):
    def __init__(self, mw, dest):
        QThread.__init__(self)
        self.mw = mw
        self.dest = dest

    def run(self):
        ftxt = open("{dest}/{title}.txt".format(dest=self.dest, title=self.mw.setting['title']), 'w')
        for s in range(self.mw.entrylist.count()):
            ew = self.mw.entrylist.getByIndex(s)
            ftxt.write("{index}. {name}\n".format(
                index=ew.index, name=ew.editors['atop'].text()))
            for i in range(0, ew.dpw):
                if ew.editors['def-%d' % (i + 1)].text() != '':
                    ftxt.write(ew.editors['def-%d' % (i + 1)].text() + '\n')
                for j in range(0, ew.epd):
                    if ew.editors['ex-%d-%d' % (i + 1, j + 1)].text() != '':
                        ftxt.write('\t' + ew.editors['ex-%d-%d' % (i + 1, j + 1)].text() + '\n')
            ftxt.write('\n')
        ftxt.close()

class HtmlThread(QThread):
    def __init__(self, mw, dest):
        QThread.__init__(self)
        self.mw = mw
        self.dest = dest

    def run(self):
        datas = [ew.data() for ew in self.mw.entrylist.getCurrentEntries()]

        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader('templates/html'))
        temp = env.get_template('words.html')
        rendered_temp = temp.render(ewDatas=datas)

        with open('{dest}/{title}.html'.format(dest=self.dest, title=self.mw.setting['title']), 'w') as f:
            f.write(rendered_temp)


class TextDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.entrylist = mw.entrylist
        self.textDir = os.path.join(mw.getProjectPath(), "text")
        self.form = gui.forms.textdialog.Ui_TextDialog()
        self.form.setupUi(self)
        self.setupList()
        self.form.startBtn.clicked.connect(self.onCreate)
        self.show()

    def setupList(self):
        imgList = self.form.imgList
        # FIXME: maxImg is not in use.
        # Look for the solution to tell DLer how many images are in short
        # according to the value of imgSpin
        maxImg = self.form.imgSpin.value()

        for i, ew in enumerate(self.entrylist.getCurrentEntries()):
            group = ew.editors['atop'].text()
            index = 2 * i + 1
            destDir = os.path.join(self.textDir, ew.getDirname())
            if group == '':
                # TODO: Change 'pass' to 'continue' on commit
                pass
            lwi1 = QListWidgetItem()
            gb = GroupButton(self.mw, group, filter="Images (*.jpg *.jpeg *.png)",
                             idx=index,
                             dir=self.mw.getProjectPath(), msg="Select an Image")
            gb.sig.connect(self.onAddImage)
            lwi1.setSizeHint(gb.sizeHint())
            lwi2, ip = QListWidgetItem(), ImagePanel(group, destDir, maxImg)
            lwi2.setSizeHint(ip.size())

            imgList.addItem(lwi1)
            imgList.setItemWidget(lwi1, gb)
            imgList.addItem(lwi2)
            imgList.setItemWidget(lwi2, ip)

    def onAddImage(self, imgpath, group, idx):
        imgList = self.form.imgList
        panel = imgList.itemWidget(imgList.item(idx))

        pixmap = QPixmap(imgpath).scaled(128, 128)
        img = QLabel()
        img.setPixmap(pixmap)
        lwi = QListWidgetItem()
        lwi.setSizeHint(img.sizeHint())
        # Insert item in front of DL button
        panel.insertItem(panel.count() - 1, lwi)
        panel.setItemWidget(lwi, img)

    def onCreate(self):
        self.th = HtmlThread(self.mw, self.textDir)
        self.th.start()
        self.th.finished.connect(lambda: self.reject())

    def reject(self):
        self.done(0)
        gui.dialogs.close("TextDialog")
