
# https://docs.microsoft.com/en-us/windows/python/beginners
# https://developers.google.com/identity/protocols/oauth2/service-account#python


from __future__ import print_function
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2 import service_account


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
HOME_PATH = str(Path.home())
SERVICE_ACCOUNT_FILE = HOME_PATH + '/devkey/devhkmci-gmaildomainwide-1d7640a0c6d2.json'

def main():


    DELEGATE='aaron.ko@dev.hkmci.com'  # Service account will impersonate this user. Must have proper admin privileges in G Suite.
    # TARGET='dev.hkmci.com'  # Service account wants to access data from this.

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    credentials_delegated = credentials.with_subject(DELEGATE)

    service = build('gmail', 'v1', credentials=credentials_delegated)

    # Call the Gmail API

    results = service.users().getProfile(userId='me').execute()
    print(results)


    results = service.users().labels().list(userId='me').execute()
    print(results)

    # labels = results.get('labels', [])

    # for label in labels:
    #     print(label['name'])

    # if not labels:
    #     print('No labels found.')
    # else:
    #     print('Labels:')
    #     for label in labels:
    #         print(label['name'])

if __name__ == '__main__':
    main()
# [END gmail_quickstart]
