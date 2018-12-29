import psycopg2, os
from app import create_app


app = create_app()

def init_db():
    """ Set up database """
    db_url = app.config['DATABASE_URL']

    conn = psycopg2.connect(db_url)

    with conn as conn, conn.cursor() as cursor:
        with app.open_resource('database.sql', mode='r') as sql:
            cursor.execute(sql.read())
        conn.commit()
        return conn

def connect_to(url):
    conn = psycopg2.connect(url)
    return conn


def _init_db():
    conn = connect_to(os.getenv('DATABASE_TESTING_URL'))
    destroy()
    with conn as conn, conn.cursor() as cursor:
        with app.open_resource('database.sql', mode='r') as sql:
            cursor.execute(sql.read())
            conn.commit()
            return conn


def destroy():
    test_url = os.getenv('DATABASE_TESTING_URL')
    conn = connect_to(test_url)
    cursor = conn.cursor()
    users = "DROP TABLE IF EXISTS users CASCADE"
    questions = "DROP TABLE IF EXISTS questions CASCADE"
    answers = "DROP TABLE IF EXISTS answers CASCADE"
    queries = [users, questions, answers]

    try:
        for query in queries:
            cursor.execute(query)
        conn.commit()
    except:
        print("Failed to destroy")