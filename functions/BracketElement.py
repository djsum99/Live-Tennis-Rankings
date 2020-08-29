#translates a number (0-127) to an array of eight bits, and the last
#bit is cut off so that BracketElements could be matched together based on
#identical bitsArrs
def position_to_seven_bits(position):
    bitsArr = []
    for i in range(8):
        bit = position%2
        bitsArr = [bit]+bitsArr
        position = int(position/2)
    return bitsArr[:-1]

'''
A BracketElement is a piece of a Tournament's bracket. Since a bracket will
always be single elimination, the size of the bracket will always be 2^n,
where n is the number of rounds. This means there will be 2^n BracketElements
in the bracket. The main identifier of the position of the BracketElement in
the bracket is the bitsArr, which translates the position of the player in the
bracket into an array of seven bits. BracketElements with identical bitsArrs
are opponents. When a match is completed, the loser's bitsArr stays the same,
while the winner's bitsArr becomes bitsArr[:-1], and the winner is then matched
with a new opponent with an identical bitsArr. If there is no other BracketElement
with an identical bitsArr, then it means either the winner won the tournament
or the opponent has not been determined yet (match still to be completed).
'''
class BracketElement:
    def __init__(self, position, newPoints):
        self.bitsArr = position_to_seven_bits(position)
        self.opponent = 'BYE'
        self.newPoints = newPoints
        self.lostTo = ''
        self.round = 0

    #for comparing BracketElements in test cases
    def __eq__(self, other) :
        return self.__dict__ == other.__dict__

    #when a player wins, their associated BracketElement updates by changing
    #the bitsArr
    def win(self):
        self.bitsArr = self.bitsArr[:-1]
        self.round += 1
