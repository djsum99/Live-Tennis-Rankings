import os
import json
import requests
from services.environment import appendOsEnvironmentVariables

# Appends environment variables to os.environ variables
appendOsEnvironmentVariables()

from services.log import log



def get_singles_rankings_request():
    response = requests.get(os.environ['ATP_SINGLE_RANKINGS_URL'])
    assert response.status_code == 200, json.dumps({
        'Event': 'get_singles_rankings_request',
        'Details': {
            'Message': 'Status code != 200',
            'StatusCode': response.status_code
        }
    })

    log.info({
        'Event': 'get_singles_rankings_request',
        'Details': {
            'Message': 'Successfully got ranking request'
        }
    })

    return response.text
