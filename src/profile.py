class Profile:
    def __init__(self, id, alias, spotted = 0, spots = 0):
        self.id = id
        self.alias = alias
        self.spotted = spotted
        self.spots = spots
        
    def changeAlias(self, alias):
        self.alias = alias
    
    def spottedSomeone(self):
        self.spots += 1

    def gotSpotted(self):
        self.spotted += 1
    
    def __repr__(self):
        return self.alias+ "\n\tspots: "+repr(self.spots)+"\tspotted: "+repr(self.spotted)