class Profile:
    def __init__(self, name, alias):
        self.name = name
        self.alias = alias
        self.spotted = 0
        self.spots = 0
    
    def changeAlias(self, alias):
        self.alias = alias
    
    def spottedSomeone(self):
        self.spots += 1

    def gotSpotted(self):
        self.spotted += 1

