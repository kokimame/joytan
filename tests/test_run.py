from .gui_testing import joytan_running

def test_initialization():
    with joytan_running() as joytan_app:
        print(dir(joytan_app))