class Profile:
    def __init__(self, name, alias):
        self.id = name
        self.alias = alias
        self.spotted = 0
        self.spots = 0
    
    def changeAlias(self, alias):
        self.alias = alias
    
    def spottedSomeone(self):
        self.spots += 1

    def gotSpotted(self):
        self.spotted += 1
    
    def __repr__(self):
        return self.alias+ "       spots:"+repr(self.spots)+"        spotted:"+repr(self.spotted)