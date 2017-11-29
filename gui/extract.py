import re

import gui
import tools.extractor as extractor
from gui.utils import getFiles


def onExtract(mw):
    filter = ";;".join([x[0] for x in extractor.Extractors])
    # Fixme: Enable to select multiple files
    files = getFiles(mw, "Extract Words from File", dir=mw.pref['worddir'], filter=filter)

    if not files:
        print("Error: File not found")
        return

    # Extract files one by one
    for file in files:
        words = extract(file)
    # Add word to frame
    for word in words:
        mw.framelist.addEntry(word, mw.frameMode)



def extract(file):
    # Various Extractor will be available for a lot of file formats
    # For now, we only extract from a file with one word in each line

    # Extractor
    exttr = None
    for e in extractor.Extractors:
        for vft in re.findall("[( ]?\*\.(.+?)[) ]", e[0]):
            # If valid file file is chosen
            if file.endswith("." + vft):
                exttr = e[1]
                break
    if not exttr:
        print("Error: Cannot open the file.")

    return exttr(file).run()
