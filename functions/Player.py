from Point import Point

class Player:
    def __init__(self, name):
        self.name = name
        self.ranking = 0
        self.points = 0
        self.tournaments = {}

    def update_tournaments(self, tournamentName, tournamentPoint):
        self.tournaments[tournamentName] = tournamentPoint


    #methods needed: choosing which points contribute to ranking, update ranking and points after each match outcome
