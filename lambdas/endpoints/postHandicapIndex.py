import json
import requests
import os

import configFile as getConfigs # Config file

# airtable
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
AIRTABLE_BASE_KEY = os.environ['AIRTABLE_BASE_KEY']
TBL_HANDICAPTRACKER = os.environ['TBL_HANDICAPTRACKER']

# Getting lastest recorded entry in AirTable
def getLatestHandicapEntry():

    # Getting entried in Handicap Tracker airtable 
    url = getConfigs.airTable_baseURI + AIRTABLE_BASE_KEY + '/' + TBL_HANDICAPTRACKER + '?'
    # print (url)
    headers = {
        'Authorization': AIRTABLE_API_KEY,
        'Content-Type' : 'application/json'
    }

    # doing GET
    resp = requests.get(url, headers=headers)
    # print (resp.status_code)
    # print (resp.content)

    entries = resp.json() # making resp. python friendly
    # print (entries)

    entries_list = [] # list to hold entries the way I want them 

    for i in entries.keys():
        for j in entries[i]:
            thisEntry = {
                "sys_createdDate": j['createdTime'],
                "entryDate": j['fields']['Entry Date'],
                "Handicap": j['fields']['Handicap']
            }
            # print (thisEntry)

            entries_list.append(thisEntry) # into the list
    
    # print (entries_list)

    sorted_entries_list = sorted(entries_list, key=lambda item: item.get("sys_createdDate"))
    # print (sorted_entries_list)

    latest_handicap_entry_dict = sorted_entries_list[-1] # latest recorded handicap entry

    return latest_handicap_entry_dict

def handler(event, context):

    # print ('we are in a lambda, triggered by step functions- woohoo')

    # print (event)

    # if == 'NA': # not enough rounds to calculate handicap
    #     print('come back to this')
    # else:
    
    print (getLatestHandicapEntry())
    