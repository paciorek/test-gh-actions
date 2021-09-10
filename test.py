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

import numpy as np
import os
from datetime import datetime

import pdb

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1G264KrXYdp4Y0YQ4IpIetbQ2ItqEwOVrhZb-KkNMiPw'
SAMPLE_RANGE_NAME = 'Sheet1!A1:D2000'
SAMPLE_RANGE_NAME2 = 'Sheet1!A2:A3'

def main():
    """Shows basic usage of the Sheets API
    """
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
        l = len(values)
        print('Found %s rows' % l-1)
        print('Last row is: %s, %s' % (values[l-1][0], values[l-1][1]))

        if values[0][3] != "processed":
            raise Exception("Fourth column in sheet is not 'processed'.")
        lens = [len(x) for x in values]
        unprocessed = np.where(np.array(lens) == 3)
        if len(unprocessed[0]) >= 1:
            ## update spreadsheet processed column
            st = np.min(unprocessed) + 1
            end = np.max(unprocessed) + 1
            insertvalues = [['yes']] * (end-st+1)
            body = {
                'values': insertvalues
            }

            SAMPLE_RANGE_OUTPUT = 'Sheet1!D' + str(st) + ':D' + str(end)
            result = sheet.values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_OUTPUT,
                valueInputOption='USER_ENTERED', body=body).execute()

            ## modify README
            now = datetime.now()
            dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
            
            numberLine = 'sed -i "s/^Number of sheet entries:.*/Number of sheet entries: ' + str(l-1) + '/" README.md'
            dateLine = 'sed -i "s/^Last entry processed:.*/Last entry processed: ' + dt_string + '/" README.md'
            
            os.system(numberLine)
            os.system(dateLine)

        if(l == 2000):
            raise Exception("Full spreadsheet not read")
        
if __name__ == '__main__':
    main()
