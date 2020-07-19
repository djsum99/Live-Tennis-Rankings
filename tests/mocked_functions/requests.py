from services.io import readFromFile

class MockedResponse:
    def __init__(self, statusCode, response):
        self.status_code = statusCode
        self.text = response

def mocked_get_request(*args, **kwargs):
    return MockedResponse(200, readFromFile('data/singles_ranking_request.html'))
    