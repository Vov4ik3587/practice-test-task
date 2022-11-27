import sys

import modules.db
import modules.sheets
import modules.emails


def sign_up_event(db_conn, service, http_auth, serv_smtp):
    print('На какое событие вы хотите записаться?')
    all_events = modules.db.all_event(db_conn)
    for (index, event) in enumerate(all_events):
        print(f"{index + 1}. Cобытие '{event[0]}', дополнительная информация по ссылке: {event[1]}")
    pick_event = int(input())
    if pick_event <= len(all_events):
        info = {
            'first_name': input('Введите имя:\n'),
            'last_name': input('Введите фамилию:\n'),
            'email': input('Введите адрес электронной почты:\n')
        }
        modules.sheets.write_to_sheet(service, http_auth, all_events[pick_event - 1], info)
        modules.db.add_db_participant(db_conn, info, all_events[pick_event - 1][3])
        modules.emails.send_email(serv=serv_smtp, info=all_events[pick_event-1], is_creator=False, participant=info)
        print('Запись прошла успешно!')
    else:
        sys.exit('Некорректный выбор')


def menu():
    # Подключение ко всем сервисам
    db_conn = modules.db.connect_db()
    service, http_auth = modules.sheets.connect_google_sheets_api('modules/creds.json')
    serv_smtp = modules.emails.connect_to_smtp()

    print('Что вы хотите сделать?')
    print('1. Создать событие')
    print('2. Записаться на существующее событие')
    pick = int(input())

    if pick == 1:
        create_event(db_conn, service, http_auth, serv_smtp)
    elif pick == 2:
        sign_up_event(db_conn, service, http_auth, serv_smtp)


def create_event(db_conn, service, http_auth, serv_smtp):
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
        modules.emails.send_email(serv=serv_smtp, info=info_event, is_creator=True)

    else:
        sys.exit('Вы не можете создать событие, так как не являетесь сотрудником')


if __name__ == '__main__':
    menu()
