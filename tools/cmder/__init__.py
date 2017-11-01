from gui.utils import isMac, isLin, isWin
import shutil



if isMac or isLin:
    assert shutil.which("cat") != None, "cat command not found."
    assert shutil.which("grep") != None, "grep command not found"
    assert shutil.which("ffmpeg") != None, "ffmpeg command not found."
    assert shutil.which("sox") != None, "sox command not found."

if isWin:
    # Fixme: How to know whether users have type command on Windows
    #assert shutil.which("type") != None, "type command not found"
    assert shutil.which("ffmpeg") != None, "ffmpeg command not found."
    pass



if isLin:
    assert shutil.which("espeak") != None, "Use espeak as default on Linux"
if isMac:
    assert shutil.which("say") != None, "Use say as default on Mac"
if isWin:
    "This is test without TTS"