import psycopg2

def connect_db():
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="test",
        user="postgres",
        password="3587"
    )
    