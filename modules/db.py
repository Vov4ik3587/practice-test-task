import psycopg2
import sshtunnel


def connect_db():
    server = sshtunnel.SSHTunnelForwarder(('ssh.cloud.nstu.ru', 5115),
                                          ssh_username='root',
                                          ssh_password='ppm0du3j',
                                          remote_bind_address=('localhost', 5432),
                                          local_bind_address=('localhost', 5432))
    server.start()

    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='3587'
    )
    # cursor = conn.cursor()
    # cursor.execute('SELECT * FROM public.kok')
    # record = cursor.fetchall()
    # conn.commit()
    # cursor.close()
    print(record)
    return conn


if __name__ == '__main__':
    connection = connect_db()
