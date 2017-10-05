class Extractor:
    def __init__(self, file):
        self.file = file

    def run(self):
        # Extractor's result should be completely independent from the application
        # This means the input is only a file and output is the list of words in the file.
        # Implementation of the run with underscore depends on file formats
        ret = self._run()
        # Verify the behaviour of subclasses
        assert type(ret) is list
        return ret


    def _run(self):
        raise NotImplementedError