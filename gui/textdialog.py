from gui.qt import *
import gui

def onTextDialog(mw):
    gui.dialogs.open("TextDialog", mw)

class TextDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.framelist = self.mw.framelist

        self.form = gui.forms.textdialog.Ui_TextDialog()
        self.form.setupUi(self)
        self.form.createBtn.clicked.connect(self.onCreate)
        self.show()

    def onCreate(self):
        from gui.utils import rmdir, mkdir
        textRoot = "{root}/text".format(root=self.mw.getRootPath())
        rmdir(textRoot)
        mkdir(textRoot)


        ftxt = open("{root}/{title}.txt".format(root=textRoot, title=self.mw.pref['title']), 'w')
        for s in range(self.framelist.count()):
            bw = self.framelist.getBundleWidget(s)
            ftxt.write("{index}. {name}\n".format(
                index=bw.index, name=bw.editors['name'].text()))
            for i in range(0, bw.dpw):
                if bw.editors['def-%d' % (i + 1)].text() != '':
                    ftxt.write(bw.editors['def-%d' % (i + 1)].text() + '\n')
                for j in range(0, bw.epd):
                    if bw.editors['ex-%d-%d' % (i + 1, j + 1)].text() != '':
                        ftxt.write('\t' + bw.editors['ex-%d-%d' % (i + 1, j + 1)].text() + '\n')
            ftxt.write('\n')
        ftxt.close()
        self.reject()

    def reject(self):
        self.done(0)
        gui.dialogs.close("TextDialog")
