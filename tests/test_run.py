from .gui_testing import joytan_running
from gui.copy import CopyDialog

def test_initialization():
    with joytan_running() as joytan_app:
        joytan_app