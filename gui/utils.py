import sys, os
from subprocess import call

import gui
from gui.qt import *


isMac = sys.platform.startswith("darwin")
isWin = sys.platform.startswith("win32")
isLin = not isMac and not isWin

class CustomLineEdit(QLineEdit):
    def __init__(self, text=''):
        super(CustomLineEdit, self).__init__(text)
        # TODO: Set the default language from Preferences
        self.langCode = 'en'

    def setForeignText(self, text, langCode):
        super().setText(text)
        self.langCode = langCode




def getFiles(parent, title, filter="*.*", dir=None):
    opts = QFileDialog.Options()
    opts |= QFileDialog.DontUseNativeDialog
    fd = QFileDialog()

    if os.path.exists(dir):
        fd.setDirectory(dir)
    fd.setOptions(opts)
    fd.setFileMode(QFileDialog.ExistingFile)
    fd.setWindowTitle(title)
    fd.setNameFilter(filter)
    fd.exec_()
    return list(fd.selectedFiles())

def getFile(parent, title, filter="*.*", dir=None):
    opts = QFileDialog.Options()
    opts |= QFileDialog.DontUseNativeDialog
    fd = QFileDialog()

    if os.path.exists(dir):
        fd.setDirectory(dir)
    fd.setOptions(opts)
    fd.setFileMode(QFileDialog.ExistingFile)
    fd.setWindowTitle(title)
    fd.setNameFilter(filter)
    fd.exec_()

    return fd.selectedFiles()[0]

def getFileNameFromPath(longpath):
    return os.path.basename(os.path.normpath(longpath))

def processCoreEvents():
    gui.app.processEvents()

def mkdir(path):
    rmdir(path)
    assert not os.path.exists(path)
    os.makedirs(path)
    print("mkdir %s" % path)

def rmdir(path):
    if isWin:
        call("rmdir {path} /s /q".format(path=path), shell=True)
    else:
        call("rm -rf {path}".format(path=path), shell=True)
    print("rmdir %s" % path)