import json
import requests
import os

import configFile as getConfigs # Config file

# airtable
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
AIRTABLE_BASE_KEY = os.environ['AIRTABLE_BASE_KEY']
TBL_ROUNDS = os.environ['TBL_ROUNDS']

def handler(event, context):

    # print ('We here')

    # Getting upcoming market holidays
    url = getConfigs.airTable_baseURI + AIRTABLE_BASE_KEY + '/' + TBL_ROUNDS + '/'
    # print (url)
    headers = {
        'Authorization': AIRTABLE_API_KEY,
        'Content-Type' : 'application/json'
    }

    # doing GET
    res = requests.get(url, headers=headers)
    # print (res.status_code)
    print (res.content)
