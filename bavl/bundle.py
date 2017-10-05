class Bundle():
    # Bundle for a word containing a number of meaning and example usage of its word
    def __init__(self, name, index):
        # A Bundle must be initialize with the index in the frame and its name.
        #
        # Bundle is free from System preferences. It has as much contents as possible.
        # Things to be rendered in the UI are chosen by FrameManager considering Preferences.
        self.index = index
        self.name = name
        self.title = None
        self.dir = None

        # TODO: Alter this var name to "DLC" related term.
        self.items = None # DLC

    def updateItems(self, items):
        self.items = items
