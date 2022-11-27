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
    values = (
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
    results = (
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

# def spreadsheet_read(service, spreadsheet_id, range):
#     values = (
#         service.spreadsheets()
#         .values()
#         .get(spreadsheetId=spreadsheet_id, range="A1:E10", majorDimension="COLUMNS")
#         .execute()
#     )
#
#     print(values)

# if __name__ == "__main__":
