# AirTable
airTable_baseURI = 'https://api.airtable.com/v0/'

# NOTEME: To keep the data transfer load to a minimum, adding filters to the URI
airTable_urlFilter1 = 'fields%5B%5D=RoundID' # Only getting the interested field, 'RoundID'
airTable_urlFilter2 = 'fields=RoundID&fields=Date&fields=HandicapDifferential' # Only getting the interested fields
