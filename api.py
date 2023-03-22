import os

import psycopg2 as psycopg2
from flask import Flask

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='flask_db',
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'],
    )
    return conn


@app.route('/')
def index():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM meetup_events LIMIT 100 ;')
            meetup_events = cursor.fetchall()

    return {'meetup_events': meetup_events}


if __name__ == '__main__':
    app.run("0.0.0.0", port=8000)
