from tools.parser.base import BaseParser

class OxfordParser(BaseParser):
    def __init__(self):
        BaseParser.__init__(self)
        self.sourceUrl = "https://en.oxforddictionaries.com/definition/"
        self.sourceName = "Oxford English Dictionary"