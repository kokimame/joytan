import os, sys
from subprocess import call

isMac = sys.platform.startswith("darwin")
isWin = sys.platform.startswith("win32")
isLin = not isMac and not isWin

def mkdir(path):
    call("rm -rf {path}".format(path=path), shell=True)
    assert not os.path.exists(path)
    os.makedirs(path)

def rmdir(path):
    call("rm -rf {path}".format(path=path), shell=True)