import sys

import modules.db
import modules.sheets
import modules.emails


def menu():
    print('Что вы хотите сделать?')
    print('1. Создать событие')
    pick = int(input())

    db_conn = modules.db.connect_db()
    service, http_auth = modules.sheets.connect_google_sheets_api('modules/creds.json')

    if pick == 1:
        create_event(db_conn, service, http_auth)


def create_event(db_conn, service, http_auth):
    print('Создаем событие...')
    info_event = {
        'first_name': input('Введите ваше Имя:\n'),
        'last_name': input('Введите вашу Фамилию:\n'),
        'email': input('Введите вашу электронную почту:\n'),
        'name_event': input('Назовите событие:\n'),
        'description_event': input('Опишите ваше событие:\n'),
        'place_event': input('Где будет проходить событие:\n'),
        'date_event': input('Дата проведения события (в формате YYYY-MM-DD):\n'),
        'time_event': input('Время начала события(в формате HH:MM:SS):\n')
    }

    if modules.db.is_employee(db_conn, info_event):
        spreadsheet_id, spreadsheet_url = modules.sheets.create_sheet(service, info_event, http_auth)
        modules.db.add_bd_event(db_conn, info_event, spreadsheet_id, spreadsheet_url)
        modules.emails.send_email(info_event, is_creator=True)

    else:
        sys.exit('Вы не можете создать событие, так как не являетесь сотрудником')


def main():
    menu()


if __name__ == '__main__':
    main()
