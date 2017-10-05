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
        # Is bundle updated? Set this False after any update
        # Fixme: Exclude all properties of the GUI side from this class
        # These conditions should be decided only in the other side.
        self.toUpdateUi = False
        self.toRender = True
        # TODO: Alter this var name to "DLC" related term.
        self.items = None # DLC

    def updateItems(self, items):
        self.items = items
        self.toUpdateUi = True
