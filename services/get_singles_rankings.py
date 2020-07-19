import os
import json
import requests
from bs4 import BeautifulSoup
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

def get_singles_rankings():
    try:
        soup = BeautifulSoup(get_singles_rankings_request())
        table = soup.findAll('tbody')[0]
        response = []
        for row in table.findAll('tr'):
            response.append([
                td.get_text(strip=True) 
                for td in row.find_all('td')
                if td.get_text(strip=True) != ''
            ])

        return response
    except Exception as e:
        log.exception(e)
        log.error({
            'Event': 'get_singles_rankings',
            'Details': {
                'Message': 'Something went wrong'
            }
        })
        raise e