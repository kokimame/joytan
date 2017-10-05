import time
from subprocess import call

def make():
    start = time.time()
    call(["python3", "make_mp3.py"])
    print("Elapsed Time: ", time.time() - start)

make()
