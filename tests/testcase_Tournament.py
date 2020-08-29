import boto3
import os
import unittest
import copy
from data.tournament import tournament, tournamentOneMatch, tournamentTwoMatches, tournamentThreeMatches

class MyTestCase(unittest.TestCase):

    def setUp(self):
        super(MyTestCase, self).setUp()

    def tearDown(self):
        super(MyTestCase, self).tearDown()

    def test_completed_match(self):
        tournamentX = copy.deepcopy(tournament)
        tournamentX.completed_match('SWill')
        assert tournamentX==tournamentOneMatch

        tournamentX.completed_match('CMcHa')
        assert tournamentX==tournamentTwoMatches
        assert tournamentX.is_bracket_completed('CMcHa')==False

        tournamentX.completed_match('SWill')
        assert tournamentX==tournamentThreeMatches
        assert tournamentX.is_bracket_completed('SWill')==True
