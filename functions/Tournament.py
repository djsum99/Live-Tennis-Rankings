from BracketElement import BracketElement
from levels import levels
from rankings import *
'''
A Tournament has the following attributes: a name, a level, and a bracket
made up of BracketElements
'''

def add_players(tournament):
    global rankings
    global players
    for player in tournament.bracket.keys():
        if player not in players.keys():
            rankings.append({"name": player, "points": 0})
            players[player] = {"ranking": 0, "points": 0, "tournaments": {}}
    sort_rankings()
    save_players()
    save_rankings()

class Tournament:
    def __init__(self, name, level, players):
        self.name = name
        self.level = level
        self.completed = False
        self.pointsDistribution = levels.get(level, 'Invalid Level')

        #bracket is a dictionary, with the key being the name of the player
        #and the value being the BracketElement associated with the player
        self.bracket = {}
        for i in range(0,len(players),2):
            self.bracket[players[i]] = BracketElement(i, self.pointsDistribution[0])
            self.bracket[players[i+1]] = BracketElement(i+1, self.pointsDistribution[0])
            self.bracket[players[i]].opponent = players[i+1]
            self.bracket[players[i+1]].opponent = players[i]

        add_players(self)

    #for comparing Tournaments in test cases
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    #determines whether the match that was just completed was the last
    #match of the tournament, thereby completing the bracket
    def is_bracket_completed(self, winnerName):
        if self.bracket[winnerName].round==len(self.pointsDistribution)-1:
            self.completed = True
            self.bracket[winnerName].opponent = 'Won Tournament'
            return True
        return False

    #updates the bracket after the completion of a match by moving
    #the winner forward and stating the loser lost to the winner
    def completed_match(self, winnerName):
        try:
            self.bracket[winnerName].win()
            self.bracket[winnerName].newPoints = self.pointsDistribution[self.bracket[winnerName].round]
            update_player(winnerName, self.name, self.pointsDistribution[self.bracket[winnerName].round])
            opponent = self.bracket[winnerName].opponent
            if not self.is_bracket_completed(winnerName):
                for key in self.bracket.keys():
                    if key!=winnerName and self.bracket[winnerName].bitsArr==self.bracket[key].bitsArr:
                        self.bracket[winnerName].opponent = key
                        self.bracket[key].opponent = winnerName
                        break
                    else:
                        self.bracket[winnerName].opponent = 'TBD'

            self.bracket[opponent].lostTo = winnerName
            self.bracket[opponent].opponent = ''
        except KeyError:
            print('winnerName not in bracket')


t = Tournament('auckland', 'i', ['SW', 'CG', 'CM', 'AL'])
t.completed_match('SW')
