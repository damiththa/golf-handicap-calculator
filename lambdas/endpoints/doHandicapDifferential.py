import json
import requests
import os

import configFile as getConfigs # Config file

# airtable
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
AIRTABLE_BASE_KEY = os.environ['AIRTABLE_BASE_KEY']
TBL_HANDICAPDIFFERENTIAL = os.environ['TBL_HANDICAPDIFFERENTIAL']

def handler(event, context):

    # print ('we are in a lambda, triggered by step functions- woohoo')

    # print (event)
    # NOTEME: This is already sorted by the lowest HandicapDefferential to highest

    # Checking No. of Rounds returned
    roundsEntered = len(event['Input'])

    # Getting stored Handicap Differential from AirTable 
    # Getting Rounds from AirTable
    url = getConfigs.airTable_baseURI + AIRTABLE_BASE_KEY + '/' + TBL_HANDICAPDIFFERENTIAL
    # print (url)
    headers = {
        'Authorization': AIRTABLE_API_KEY,
        'Content-Type' : 'application/json'
    }

    # doing GET
    resp = requests.get(url, headers=headers)
    # print (resp.status_code)
    # print (resp.content)

    # Into a python array in HandicapDefferential in desc. order 
    handicapDifferential = resp.json() # making resp. python friendly
    # print (handicapDifferential)

    handicapDifferential_dict = {} # dict. to hold values

    for k in handicapDifferential['records']:
        # print (k['fields']['No. Rounds Entered']) 
        # print (k['fields']['Lowest differentials to Use'])
        handicapDifferential_dict[k['fields']['No. Rounds Entered']] = k['fields']['Lowest differentials to Use']

    # print (handicapDifferential_dict)
    # Ex --> {'12': '4', '17': '7', '14': '5', '4': '0', '18': '8', '16': '6', '8': '2', '6': '1', '10': '3', '19': '9', '20': '10'}

    handicapDifferential_dict_keys = list(handicapDifferential_dict.keys())
    #Ex --> ['12', '17', '14', '4', '18', '16', '8', '6', '10', '19', '20']
    handicapDifferential_dict_keys = [int(i) for i in handicapDifferential_dict_keys] # converting list of Strings into a int
    # print (handicapDifferential_dict_keys)
    #Ex --> [12, 17, 14, 4, 18, 16, 8, 6, 10, 19, 20]

    # checking no. if entered rounds is more than number of rounds needed for lowest handicap differential
    if roundsEntered <= max(handicapDifferential_dict_keys):
        lowest_num_rounds = min([i for i in handicapDifferential_dict_keys if roundsEntered <= i]) 
        # See more --> https://stackoverflow.com/a/36275519/789782
        # print (lowest_num_rounds)
    else:
        lowest_num_rounds = max(handicapDifferential_dict_keys) # this is 20

    diff_to_use = int(handicapDifferential_dict[str(lowest_num_rounds)]) # lowest handicap differential to use
    # print (diff_to_use)

    # Finding Handicap Index
    if diff_to_use != 0:
        # print (diff_to_use)

        rounds_to_use_dict = list(event['Input'])[0:diff_to_use]
        # print (rounds_to_use_dict)

        rounds_to_use_total = sum(d['HandicapDifferential'] for d in rounds_to_use_dict)
        # print (rounds_to_use_total)

        rounds_to_use_average = rounds_to_use_total / diff_to_use
        # print (rounds_to_use_average)

        handicap_index = round(rounds_to_use_average * getConfigs.usga_handicap_index_constant, 2)
        print (handicap_index)

    else: # handicap differentail is 0
        print ('COME BACK AND DO THIS ')



    
