import gui
from gui.qt import *
from gui.widgets.groupbtn import GroupButton
from gui.widgets.imgpanel import *

def onTextDialog(mw):
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
            ew = self.mw.entrylist.getByIndex(i + 1)
            ftxt.write("{index}. {name}\n".format(
                index=ew.index, name=ew.editors['atop'].text()))
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
        datas = [ew.data() for ew in self.mw.entrylist.getEntries()]

        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader('templates/html'))
        temp = env.get_template('words.html')
        rendered_temp = temp.render(entries=datas)

        with open('{dest}/{title}.html'.format(dest=self.dest, title=self.mw.setting['title']), 'w') as f:
            f.write(rendered_temp)

class BookInfo(QWidget):
    pass

class TextDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
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
        maxImg = 4

        for i, ew in enumerate(self.mw.entrylist.getEntries()):
            group = ew.editors['atop'].text()
            index = 2 * i + 1
            destDir = os.path.join(self.textDir, ew.stringIndex())
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
        panel.images.append(imgpath)

    def getPanel(self, i):
        form = self.form
        return form.imgList.itemWidget(form.imgList.item(2 * i + 1))


    def onCreate(self):
        datas = []
        for i, ew in enumerate(self.mw.entrylist.getEntries()):
            data = ew.data()
            panel = self.getPanel(i)
            for j, img in enumerate(panel.images):
                data['img-%d' % (j + 1)] = img
            datas.append(data)


        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader('templates/html'))
        temp = env.get_template('words.html')
        rendered_temp = temp.render(entries=datas)

        with open('{dest}.html'.format(dest=self.textDir), 'w', encoding='utf-8') as f:
            f.write(rendered_temp)

    def reject(self):
        self.done(0)
        gui.dialogs.close("TextDialog")
