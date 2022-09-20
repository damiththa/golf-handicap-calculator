import json
import requests
import os

import configFile as getConfigs # Config file

# airtable
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
AIRTABLE_BASE_KEY = os.environ['AIRTABLE_BASE_KEY']
TBL_HANDICAPDIFFERENTIAL = os.environ['TBL_HANDICAPDIFFERENTIAL']

handicap_index = 'NA' # default value. This is also what will be sent when 'diff_to_use' is 0

def handler(event, context):

    print ('we are in a lambda, triggered by step functions- woohoo')

    print (event)
    