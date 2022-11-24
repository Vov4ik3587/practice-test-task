import os

import psycopg2
import sshtunnel
from dotenv import load_dotenv


def add_bd_event(db_conn, info):
    with db_conn:
        with db_conn.cursor() as cur:
            # insert into events (name, description, place, date_event, creator, time_event)
            # values ('Kok', 'joj', 'here', '2022-04-12','pm93.galstyan@gmail.com', '13:00:00');
            cur.execute(
                'INSERT INTO events (name, description, place, date_event, creator, time_event) values (%s, %s, %s, '
                '%s, %s, %s)',
                (info['name_event'], info['description_event'], info['place_event'], info['date_event'], info['email'],
                 info['time_event']))


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
        user=os.environ.get('USER'),
        password=os.environ.get('USER_PASSWORD')
    )
    return conn


if __name__ == '__main__':
    connection = connect_db()
