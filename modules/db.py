import psycopg2
import sshtunnel
from dotenv import load_dotenv
import os


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
    # cursor = conn.cursor()
    # cursor.execute('SELECT * FROM public.employees')
    # record = cursor.fetchall()
    # conn.commit()
    # cursor.close()
    # print(record)
    return conn


if __name__ == '__main__':
    connection = connect_db()
