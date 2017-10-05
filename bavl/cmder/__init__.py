from bavl.utils import isMac, isLin, isWin
import shutil

assert shutil.which("cat") != None, "cat not found."
assert shutil.which("ffmpeg") != None, "ffmpeg not found."
assert shutil.which("sox") != None, "sox not found."

if isLin:
    assert shutil.which("espeak") != None, "Use espeak as default on Linux"

if isMac:
    assert shutil.which("say") != None, "Use say as default on Mac"

if isWin:
    assert False, "Sorry, we don't support Windows for now!"
