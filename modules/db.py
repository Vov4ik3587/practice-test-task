import os
from pprint import pprint

import psycopg2
import sshtunnel
from dotenv import load_dotenv


def connect_db():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    server = sshtunnel.SSHTunnelForwarder((os.environ.get('SSH_DOMAIN'), 5115),
                                          ssh_username=os.environ.get('SSH_USERNAME'),
                                          ssh_password=os.environ.get('SSH_PASSWORD'),
                                          remote_bind_address=('localhost', 5432),
                                          local_bind_address=('localhost', 5432))
    server.start()
    conn = psycopg2.connect(
        host='localhost',
        database=os.environ.get('DATABASE'),
        user=os.environ.get('DB_USER_NAME'),
        password=os.environ.get('DB_USER_PASSWORD')
    )
    return conn


def is_employee(db_conn, info):
    with db_conn, db_conn.cursor() as cur:
        cur.execute('SELECT * FROM public.employees WHERE email=%s', (info['email'],))
        return cur.fetchone()


def add_bd_event(db_conn, info, spreadsheet_id, spreadsheet_url):
    with db_conn, db_conn.cursor() as cur:
        cur.execute(
            'INSERT INTO public.events (name, description, place, date_event, creator, time_event, '
            'spreadsheet_url, spreadsheet_id) '
            'values (%s, %s, %s, %s, %s, %s, %s, %s)',
            (info['name_event'], info['description_event'], info['place_event'], info['date_event'], info['email'],
             info['time_event'], spreadsheet_url, spreadsheet_id))


def all_event(db_conn):
    with db_conn, db_conn.cursor() as cur:
        cur.execute(
            'SELECT name, spreadsheet_url, spreadsheet_id, id_event, creator FROM events'
        )
        result = cur.fetchall()
    return result


def add_db_participant(db_conn, info, event_id):
    if is_employee(db_conn, info):
        with db_conn, db_conn.cursor() as cur:
            cur.execute(
                'INSERT INTO public.events_entrys (id_event, email) VALUES (%s, %s)', (event_id, info['email'])
            )
    else:
        with db_conn, db_conn.cursor() as cur:
            cur.execute(
                'INSERT INTO public.events_entrys (id_event, email) VALUES (%s, %s)', (event_id, info['email'])
            )
        with db_conn, db_conn.cursor() as cur:
            cur.execute(
                'INSERT INTO public.outsiders (first_name, last_name, email) VALUES (%s, %s, %s)',
                (info['first_name'], info['last_name'], info['email'])
            )


if __name__ == '__main__':
    connection = connect_db()
    res = all_event(connection)
