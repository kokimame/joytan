from bavl.extractor.base import Extractor

class NewlineExtractor(Extractor):
    def __init__(self, file):
        Extractor.__init__(self, file)

    def _run(self):
        with open(self.file, 'r') as f:
            fileContent = f.readlines()
        return [line.strip() for line in fileContent]