
# https://docs.microsoft.com/en-us/windows/python/beginners
# https://developers.google.com/identity/protocols/oauth2/GMAIL-account#python


from __future__ import print_function
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2 import service_account


SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
    ]
HOME_PATH = str(Path.home())
SERVICE_ACCOUNT_FILE = HOME_PATH + '/devkey/devhkmci-gmaildomainwide-1d7640a0c6d2.json'
SHEETS_FILE_ID = '1CIpaJuibLaA6YYpMq9l34yHqEv4KoiUlvszU6PnXRXs'
# test file: https://docs.google.com/spreadsheets/d/1CIpaJuibLaA6YYpMq9l34yHqEv4KoiUlvszU6PnXRXs/edit#gid=0


def main():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    credentials_delegated = credentials.with_subject('andersen@dev.hkmci.com')
    SHEETS = build('sheets', 'v4', credentials=credentials_delegated)


    ssvalues = SHEETS.spreadsheets().values().get(spreadsheetId=SHEETS_FILE_ID, range='Sheet1').execute().get('values')
    columns = ssvalues[0]
    print(columns) # ['email', 'messageTotal', 'threadsTotal']
    rows = ssvalues[1:] # skip header row
    values = []
    for r in rows:
        print(r)
        credentials_delegated = credentials.with_subject(r[0])
        GMAIL = build('gmail', 'v1', credentials=credentials_delegated)
        results = GMAIL.users().getProfile(userId='me').execute()
        values.append([results['messagesTotal'], results['threadsTotal']])

    print(values)

    body = {
        'values': values
    }
    result = SHEETS.spreadsheets().values().update(spreadsheetId=SHEETS_FILE_ID, range='B2:C'+str(len(values)+1), valueInputOption='USER_ENTERED', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


if __name__ == '__main__':
    main()
# [END gmail_quickstart]
