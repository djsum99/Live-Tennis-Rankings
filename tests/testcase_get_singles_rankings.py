import sys
import os
import unittest
from unittest import mock

sys.path.insert(1, os.path.abspath(os.path.dirname(os.path.join(os.path.abspath(__file__), '../../'))))
sys.path.insert(1, os.path.abspath(os.path.dirname(os.path.join(os.path.abspath(__file__), '../'))))

from services.io import readFromFile
from services.get_singles_rankings import get_singles_rankings_request

from tests.mocked_functions.requests import mocked_get_request

class ThisTestCase(unittest.TestCase):
    def setUp(self):
        self.singles_rankings_response = readFromFile('data/singles_ranking_request.html')

    @mock.patch(
        'services.get_singles_rankings.requests.get',
        side_effect=mocked_get_request
    )
    def test_get_singles_rankings_request(self, *args, **kwargs):
        response = get_singles_rankings_request()
        assert response == self.singles_rankings_response
