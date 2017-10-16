from tools.parser.dictionarycom import DictionaryComParser
from tools.parser.cambridge import CambridgeParser
from tools.parser.oxford import OxfordParser
from tools.parser.wiktionary import WiktionaryParser

Parsers = {
    "Dictionary.com": DictionaryComParser,
    "Cambridge Dictionary": CambridgeParser,
    "Oxford English Dictionary": OxfordParser,
    "Wiktionary": WiktionaryParser
}
