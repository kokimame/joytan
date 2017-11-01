from gui.utils import isMac, isLin, isWin
import shutil



if isMac or isLin:
    assert shutil.which("cat") != None, "cat command not found."
    assert shutil.which("awk") != None, "awk command not found"
    assert shutil.which("grep") != None, "grep command not found"
    assert shutil.which("ffmpeg") != None, "ffmpeg command not found."
    assert shutil.which("sox") != None, "sox command not found."

if isWin:
    # Fixme: How to know whether users have type command on Windows
    #assert shutil.which("type") != None, "type command not found"
    assert shutil.which("ffmpeg") != None, "ffmpeg command not found."
    assert shutil.which("findstr") != None, "findstr command not found"
    pass



if isLin or isWin:
    assert shutil.which("espeak") != None, "We use espeak command as default on Linux and Windows"
if isMac:
    assert shutil.which("say") != None, "We use say command as default on Mac"