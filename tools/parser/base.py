class BaseParser:
    def __init__(self):
        # Each Parser class prefers to be instantiated only one time
        # in a downloading session. This leads to make Parser to be initialized
        # without HTML data to parse. Every HTML will be passed in run method.

        # Every parser has its own source. e.g, Online dictionaries
        self.sourceUrl = None
        self.sourceName = None

    def run(self, data):
        """
        :param: data - HTML data to parse
        :return: Dictionary contents to be stored in the entries
        All Parser classes need to overwrite this method.
        Do parsing and return contents as much as possible.
        Do only one parsing for a word even if Entry preference modified
        after the parsing session.
        Each class uses a parsing method specific to their target dictionary.
        """
        raise NotImplementedError