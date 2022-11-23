import os
from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'creds.json'

class GSheet:

    

    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
    ]
    
    service = None

    def __init__(self) -> None:
        if os.path.exists('creds.json'):
            creds = ServiceAccountCredentials(CREDENTIALS_FILE, scopes=self.SCOPES)
            httpAuth = creds.authorize(httplib2.Http())
            self.service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
    

if __name__ == '__main__':
    gs = GSheet()
    values = gs.service.spreadsheets().values().get(
        spreadsheetId='1zZdLNLu6ntbXlS-A8pghN2TdORJQNPKvhVgvji8pMYI',
        range='A1:B3',
        majorDimension='COLUMNS'
        ).execute()
    pprint(values)
