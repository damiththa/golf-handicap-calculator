import json
import requests
import os

from datetime import datetime

import configFile as getConfigs # Config file

# airtable
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
AIRTABLE_BASE_KEY = os.environ['AIRTABLE_BASE_KEY']
TBL_HANDICAPTRACKER = os.environ['TBL_HANDICAPTRACKER']

# Getting lastest recorded entry in AirTable
def getLatestHandicapEntry():

    # Getting entried in Handicap Tracker airtable 
    url = getConfigs.airTable_baseURI + AIRTABLE_BASE_KEY + '/' + TBL_HANDICAPTRACKER 
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

# Adding to handicap tracker with the new handicap
def addToHandicapTracker(handicapNow):
    
    # Into an object so to be passed in as the POST body
    nowHandicapEntry = {
      "fields": {
        "Handicap": handicapNow,
        "Entry Date": json.dumps(datetime.now(), default=str) # To avoid python's JSON serializable error See --> https://stackoverflow.com/a/70960730/789782
      }
    }
    # print (nowHandicapEntry)
    # Ex. --> {'fields': {'Handicap': 23.13, 'Entry Date': '"2022-09-21 16:00:01.379476"'}}

    # POSTing to Handicap Tracker airtable 
    url = getConfigs.airTable_baseURI + AIRTABLE_BASE_KEY + '/' + TBL_HANDICAPTRACKER
    # print (url)
    headers = {
        'Authorization': AIRTABLE_API_KEY,
        'Content-Type' : 'application/json'
    }
    payload = {
        "records" : [nowHandicapEntry]
    }

    # doing POST
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    # print (res.status_code)
    # print (res.content)


def handler(event, context):

    # print ('we are in a lambda, triggered by step functions- woohoo')

    # print (event)

    calculated_handicap = event['Input'] # Just now calculated handicap

    if calculated_handicap == 'NA': # not enough rounds to calculate handicap
        print('come back to this')

    else:
        recorded_handicap_dict = getLatestHandicapEntry() # getting lastest recorded handicap

        # Comparing handicaps (recorded and calculated just now) for changes 
        if recorded_handicap_dict['Handicap'] != calculated_handicap:
            addToHandicapTracker(calculated_handicap)
    