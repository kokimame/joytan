from bavl.extractor.base import Extractor

class NewlineExtractor(Extractor):
    def __init__(self, file):
        Extractor.__init__(self, file)

    def _run(self):
        # Return the list of words in a given file.
        # The run with underscore is only called from the base's run method
        with open(self.file, 'r') as f:
            fileContent = f.readlines()
        return [line.strip() for line in fileContent]