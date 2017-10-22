from tools.parser.base import BaseParser

class OxfordParser(BaseParser):
    def __init__(self):
        BaseParser.__init__(self)
        self.source = "https://en.oxforddictionaries.com/definition/"