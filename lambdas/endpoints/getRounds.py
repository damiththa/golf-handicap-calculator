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

    # Getting Rounds from AirTable
    url = getConfigs.airTable_baseURI + AIRTABLE_BASE_KEY + '/' + TBL_ROUNDS + '?' + getConfigs.airTable_urlFilter2
    # print (url)
    headers = {
        'Authorization': AIRTABLE_API_KEY,
        'Content-Type' : 'application/json'
    }

    # doing GET
    resp = requests.get(url, headers=headers)
    # print (resp.status_code)
    # print (resp.content)

    # FIXME: This brings entries per page (less than 100), need to consider and put in a fix to accomodate pagination
    
    # Into a python array in HandicapDefferential in desc. order 
    entries = resp.json() # making resp. python friendly
    # print (entries)

    entries_list = [] # list to hold entries the way I want them 

    for i in entries.keys():
        for j in entries[i]:
            thisEntry = {
                "entryDate": j['fields']['Date'],
                "HandicapDifferential": round(j['fields']['HandicapDifferential'], 4)
            }
            # print (thisEntry)

            entries_list.append(thisEntry) # into the list
    
    # print (entries_list)

    sorted_entries_list = sorted(entries_list, key=lambda item: item.get("HandicapDifferential"))
    # print (sorted_entries_list)

    return sorted_entries_list