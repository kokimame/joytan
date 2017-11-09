from tools.parser.base import BaseParser

class CambridgeParser(BaseParser):
    def __init__(self):
        BaseParser.__init__()
        self.sourceUrl = "http://dictionary.cambridge.org/dictionary/english/"
        self.sourceName = "Cambridge Dictionary"