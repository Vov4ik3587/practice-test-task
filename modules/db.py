import psycopg2

def connect_db():
    conn = psycopg2.connect(
        host='localhost',
        database='test',
        user='postgres',
        password='3587'
    )
    # cursor = conn.cursor()
    # cursor.execute('SELECT * FROM public.employees')        
    # record = cursor.fetchall()
    # conn.commit()
    # cursor.close()
    return conn
    
if __name__ == '__main__':
    connection = connect_db()