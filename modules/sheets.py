from pprint import pprint

import apiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials


# def open_sheet(service, httpAuth):


def create_sheet(service, info, httpAuth):
    new_spreadsheet = (
        service.spreadsheets()
        .create(
            body={
                "properties": {"title": info['name_event'], "locale": "ru_RU"},
                "sheets": [
                    {
                        "properties": {
                            "sheetType": "GRID",
                            "sheetId": 0,
                            "title": 'Главное',
                            "gridProperties": {"rowCount": 150, "columnCount": 10},
                        }
                    }
                ],
            }
        )
        .execute()
    )
    pprint(f"URL созданной таблицы {new_spreadsheet['spreadsheetUrl']}")

    # Выдача доступа на чтение кому угодно
    driveService = apiclient.discovery.build("drive", "v3", http=httpAuth)
    _ = (
        driveService.permissions()
        .create(
            fileId=new_spreadsheet["spreadsheetId"],
            body={"type": "anyone", "role": "reader"},
            fields="id",
        )
        .execute()
    )
    return new_spreadsheet["spreadsheetId"], new_spreadsheet['spreadsheetUrl']


def connect_google_sheets_api(creds):
    CREDENTIALS_FILE = creds
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build("sheets", "v4", http=httpAuth)
    return service, httpAuth


def spreadsheet_write(service, spreadsheet_id, range, values):
    values = (
        service.spreadsheets()
        .values()
        .batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {
                        "range": "B3:C4",
                        "majorDimension": "ROWS",
                        "values": [
                            ["This is B3", "This is C3"],
                            ["This is B4", "This is C4"],
                        ],
                    },
                    {
                        "range": "D5:E6",
                        "majorDimension": "COLUMNS",
                        "values": [
                            ["This is D5", "This is D6"],
                            ["This is E5", "=5+5"],
                        ],
                    },
                ],
            },
        )
        .execute()
    )


def spreadsheet_read(service, spreadsheet_id, range):
    values = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range="A1:E10", majorDimension="COLUMNS")
        .execute()
    )

    pprint(values)


def main():
    service, http_auth = connect_google_sheets_api("creds.json")
    info = "New Event"
    spreadsheet_id = create_sheet(service, info, http_auth)


if __name__ == "__main__":
    main()
