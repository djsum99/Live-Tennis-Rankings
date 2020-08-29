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
tournament = Tournament('auckland', 'international', players)

tournamentOneMatch = copy.deepcopy(tournament)
tournamentOneMatch.bracket['SWill'].bitsArr = tournamentOneMatch.bracket['SWill'].bitsArr[:-1]
tournamentOneMatch.bracket['SWill'].opponent = 'TBD'
tournamentOneMatch.bracket['CGior'].lostTo = 'SWill'
tournamentOneMatch.bracket['CGior'].opponent = ''

tournamentTwoMatches = copy.deepcopy(tournamentOneMatch)
tournamentTwoMatches.bracket['CMcHa'].bitsArr = tournamentTwoMatches.bracket['CMcHa'].bitsArr[:-1]
tournamentTwoMatches.bracket['CMcHa'].opponent = 'SWill'
tournamentTwoMatches.bracket['SWill'].opponent = 'CMcHa'
tournamentTwoMatches.bracket['ALi'].lostTo = 'CMcHa'
tournamentTwoMatches.bracket['ALi'].opponent = ''

tournamentThreeMatches = copy.deepcopy(tournamentTwoMatches)
tournamentThreeMatches.bracket['SWill'].bitsArr = tournamentThreeMatches.bracket['SWill'].bitsArr[:-1]
tournamentThreeMatches.bracket['SWill'].opponent = 'Won Tournament'
tournamentThreeMatches.bracket['CMcHa'].lostTo = 'SWill'
tournamentThreeMatches.bracket['CMcHa'].opponent = ''
tournamentThreeMatches.completed = True
