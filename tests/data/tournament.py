import os
import sys
import inspect
import copy
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
from functions.Tournament import Tournament
from functions.BracketElement import BracketElement

players = ['SWill','CGior','CMcHa','ALi']
i = [1, 30, 60]
tournament = Tournament('auckland', 'i', players)
tournament.pointsDistribution = i

tournamentOneMatch = copy.deepcopy(tournament)
tournamentOneMatch.bracket['SWill'].bitsArr = tournamentOneMatch.bracket['SWill'].bitsArr[:-1]
tournamentOneMatch.bracket['SWill'].round += 1
tournamentOneMatch.bracket['SWill'].newPoints = i[tournamentOneMatch.bracket['SWill'].round]
tournamentOneMatch.bracket['SWill'].opponent = 'TBD'
tournamentOneMatch.bracket['CGior'].lostTo = 'SWill'
tournamentOneMatch.bracket['CGior'].opponent = ''

tournamentTwoMatches = copy.deepcopy(tournamentOneMatch)
tournamentTwoMatches.bracket['CMcHa'].bitsArr = tournamentTwoMatches.bracket['CMcHa'].bitsArr[:-1]
tournamentTwoMatches.bracket['CMcHa'].round += 1
tournamentTwoMatches.bracket['CMcHa'].newPoints = i[tournamentTwoMatches.bracket['CMcHa'].round]
tournamentTwoMatches.bracket['CMcHa'].opponent = 'SWill'
tournamentTwoMatches.bracket['SWill'].opponent = 'CMcHa'
tournamentTwoMatches.bracket['ALi'].lostTo = 'CMcHa'
tournamentTwoMatches.bracket['ALi'].opponent = ''

tournamentThreeMatches = copy.deepcopy(tournamentTwoMatches)
tournamentThreeMatches.bracket['SWill'].bitsArr = tournamentThreeMatches.bracket['SWill'].bitsArr[:-1]
tournamentThreeMatches.bracket['SWill'].round += 1
tournamentThreeMatches.bracket['SWill'].newPoints = i[tournamentThreeMatches.bracket['SWill'].round]
tournamentThreeMatches.bracket['SWill'].opponent = 'Won Tournament'
tournamentThreeMatches.bracket['CMcHa'].lostTo = 'SWill'
tournamentThreeMatches.bracket['CMcHa'].opponent = ''
tournamentThreeMatches.completed = True

'''
tournament.completed_match('SWill')
print(tournament.bracket==tournamentOneMatch.bracket)

for k in tournament.bracket:
    print(k+': ('+str(tournament.bracket[k].bitsArr)+', '+str(tournament.bracket[k].round)+', '+str(tournament.bracket[k].opponent)+', '+str(tournament.bracket[k].newPoints)+', '+tournament.bracket[k].lostTo+')')
for k in tournamentOneMatch.bracket:
    print(k+': ('+str(tournamentOneMatch.bracket[k].bitsArr)+', '+str(tournamentOneMatch.bracket[k].round)+', '+str(tournamentOneMatch.bracket[k].opponent)+', '+str(tournamentOneMatch.bracket[k].newPoints)+', '+tournamentOneMatch.bracket[k].lostTo+')')
'''
