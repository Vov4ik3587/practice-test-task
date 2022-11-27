from pprint import pprint

import apiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials


# def open_sheet(service, httpAuth):
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
                            "title": 'Main',
                            "gridProperties": {"rowCount": 150, "columnCount": 10},
                        }
                    }
                ],
            }
        )
        .execute()
    )

    # Выдача доступа на чтение кому угодно
    # TODO: выдавать на чтение только создателю и участникам

    drive_service = apiclient.discovery.build("drive", "v3", http=httpAuth)
    _ = (
        drive_service.permissions()
        .create(
            fileId=new_spreadsheet["spreadsheetId"],
            body={"type": "anyone", "role": "reader"},
            fields="id",
        )
        .execute()
    )

    # Заполняем пустую таблицу информацией
    spreadsheet_template(service, new_spreadsheet['spreadsheetId'], info)

    print(f"URL созданной таблицы {new_spreadsheet['spreadsheetUrl']}")

    return new_spreadsheet['spreadsheetId'], new_spreadsheet['spreadsheetUrl']


def spreadsheet_template(service, spreadsheet_id, info):
    # Заполняем таблицу данными
    _ = (
        service.spreadsheets()
        .values()
        .batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {
                        "range": "A1:D6",
                        "majorDimension": "ROWS",
                        "values": [
                            ['Название события', info['name_event']],
                            ['Описание события', info['description_event']],
                            ['Место проведения', info['place_event']],
                            ['Дата и время проведения', info['date_event'], info['time_event']],
                            ['Создатель события', info['first_name'], info['last_name'], info['email']],
                            ['Учатники события:']
                        ],
                    },
                ],
            },
        ).execute()
    )
    # меняем размер ячеек
    _ = (
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                'requests': [
                    {
                        "updateDimensionProperties": {
                            "range": {
                                "sheetId": 0,
                                "dimension": "COLUMNS",
                                "startIndex": 0,
                                "endIndex": 4
                            },
                            "properties": {
                                "pixelSize": 300
                            },
                            "fields": "pixelSize"
                        }
                    }
                ]
            }
        ).execute()
    )


def write_to_sheet(service, http_auth, event, info):
    empty_row = find_empty_cells(service, event[2])

    _ = (
        service.spreadsheets()
        .values()
        .batchUpdate(
            spreadsheetId=event[2],
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {
                        "range": f"B{empty_row}:D{empty_row}",
                        "majorDimension": "ROWS",
                        "values": [
                            [info['first_name'], info['last_name'], info['email']]
                        ]
                    },
                ],
            },
        ).execute()
    )


def find_empty_cells(service, spreadsheet_id):
    start_index = 1
    range = f"A{start_index}:D{start_index}"
    val = spreadsheet_read(service, spreadsheet_id, range)
    while 'values' in val:
        range = f"A{start_index}:D{start_index}"
        val = spreadsheet_read(service, spreadsheet_id, range)
        start_index += 1
    row_empty_cell = start_index - 1
    return row_empty_cell


def spreadsheet_read(service, spreadsheet_id, need_range):
    values = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=need_range, majorDimension="COLUMNS")
        .execute()
    )
    return values


if __name__ == "__main__":
    serv, http_auth = connect_google_sheets_api('creds.json')
    curr_row = find_empty_cells(serv, '1b-UsZcB1kVV_BmlIz_XQmKlm2JU5vNcEONZSaNhWzi0')

