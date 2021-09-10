#!/usr/bin/env python

## need to create a service account under a project (e.g., GVM0),
## enable API access in the service account, grant user access
## get credentials.json by creating an OAuth client id (I called it Desktop client)
## this then will open an authentication browser window where I can use various user IDs
## So the idea is the app I am creating will work for any user.

## pip install --user --upgrade google-api-python-client google-auth-oauthlib
## pip install  --user --upgrade google-auth
## pip install --user --upgrade cachetools
## pip install --user --upgrade oauthlib

import os.path
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

import pdb

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1G264KrXYdp4Y0YQ4IpIetbQ2ItqEwOVrhZb-KkNMiPw'
SAMPLE_RANGE_NAME = 'Sheet1!A2:B2'
SAMPLE_RANGE_NAME2 = 'Sheet1!A2:A3'

def main():
    """Shows basic usage of the Sheets API, including inserting values into 
    a copy of the Fall 2020 registration spreadsheet.
    """
    creds = None

    creds = Credentials.from_service_account_file('service_account.json', scopes = SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Field1, Field2:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[1]))

if __name__ == '__main__':
    main()
