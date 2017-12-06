import gui
from gui.qt import *
from gui.customs.groupbtn import GroupButton

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
        self.entrylist = self.mw.entrylist

        self.form = gui.forms.textdialog.Ui_TextDialog()
        self.form.setupUi(self)
        self.setupList()
        self.form.startBtn.clicked.connect(self.onCreate)
        self.show()

    def setupList(self):
        imgList = self.form.imgList
        for ew in self.entrylist.getCurrentEntries():
            lwi, gb = QListWidgetItem(), GroupButton(self.mw, ew.editors['atop'].text())
            lwi.setSizeHint(gb.sizeHint())
            imgList.addItem(lwi)
            imgList.setItemWidget(lwi, gb)



    def onCreate(self):
        textDest = "{dest}".format(dest=self.mw.setting['workspace'])

        self.th = HtmlThread(self.mw, textDest)
        self.th.start()
        self.th.finished.connect(lambda: self.reject())

    def reject(self):
        self.done(0)
        gui.dialogs.close("TextDialog")
