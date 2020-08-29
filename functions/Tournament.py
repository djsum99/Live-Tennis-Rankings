from functions.BracketElement import BracketElement
from math import log2

'''
A Tournament has the following attributes: a name, a level, a boolean
that states whether is has been completed, and a bracket made up of
BracketElements
'''
class Tournament:
    def __init__(self, name, level, players):
        self.name = name
        self.level = level
        self.completed = False

        #bracket is a dictionary, with the key being the name of the player
        #and the value being the BracketElement associated with the player
        self.bracket = {}
        for i in range(0,len(players),2):
            self.bracket[players[i]] = BracketElement(i)
            self.bracket[players[i+1]] = BracketElement(i+1)
            self.bracket[players[i]].opponent = players[i+1]
            self.bracket[players[i+1]].opponent = players[i]

    #for comparing Tournaments in test cases
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    #determines whether the match that was just completed was the last
    #match of the tournament, thereby completing the bracket
    def is_bracket_completed(self, winnerName):
        targetLength = 6-log2(len(self.bracket))
        if len(self.bracket[winnerName].bitsArr)==targetLength:
            self.completed = True
            self.bracket[winnerName].opponent = 'Won Tournament'
            return True
        return False

    #updates the bracket after the completion of a match by moving
    #the winner forward and stating the loser lost to the winner
    def completed_match(self, winnerName):
        try:
            self.bracket[winnerName].win()
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
        except:
            print('winnerName not in bracket')
