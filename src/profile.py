class Profile:
    def __init__(self, id, alias, spotted = 0, spots = 0):
        self.id = id
        self.alias = alias
        self.spotted = spotted
        self.spots = spots
        self.spotStreak = 0
        
    def changeAlias(self, alias):
        self.alias = alias
    
    def spottedSomeone(self):
        self.spotStreak += 1
        self.spots += 1

    def gotSpotted(self):
        self.spotStreak = 0
        self.spotted += 1

    def getSpotRatio(self):
        if self.spotted == 0:
            return -1
        else:
            return self.spots / self.spotted

    def getNetSpots(self):
        return self.spots - self.spotted
    
    def leaderboardInfo(self):
        return """{}
        spots: {}   spotted: {}   ratio: {:.2f}""".format(self.alias, self.spots, self.spotted, self.getSpotRatio())

    def streakInfo(self):
        return"""{}
        spot streak: {}""".format(self.alias, self.spotStreak)