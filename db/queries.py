# db/queries.py

from db.connection import get_connection


def query_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Products')
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()
