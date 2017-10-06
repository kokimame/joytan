from bavl.parser.dictionarycom import DictionaryComParser
from bavl.parser.cambridge import CambridgeParser
from bavl.parser.oxford import OxfordParser
from bavl.parser.wiktionary import WiktionaryParser

Parsers = {
    "Dictionary.com": DictionaryComParser,
    "Cambridge Dictionary": CambridgeParser,
    "Oxford English Dictionary": OxfordParser,
    "Wiktionary": WiktionaryParser
}
