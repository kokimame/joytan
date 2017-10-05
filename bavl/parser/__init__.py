from bavl.parser.dictionarycom import DictionaryComParser
from bavl.parser.cambridge import CambridgeParser
from bavl.parser.oxford import OxfordParser
from bavl.parser.wiktionary import WiktionaryParser

Parsers = {
    "dictionary-com": DictionaryComParser,
    "cambridge": CambridgeParser,
    "oxford": OxfordParser,
    "wiktionary": WiktionaryParser
}
