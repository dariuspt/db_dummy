# db/data.py

from db.connection import get_connection


def insert_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Example insertion
    cursor.execute('''
    INSERT INTO Categories (CategoryID, CategoryName) VALUES (1, 'Electronics');
    ''')

    conn.commit()
    cursor.close()
    conn.close()


def update_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Example update
    cursor.execute('''
    UPDATE Products SET Price = 899.99 WHERE ProductID = 1;
    ''')

    conn.commit()
    cursor.close()
    conn.close()


def delete_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Example delete
    cursor.execute('''
    DELETE FROM Products WHERE ProductID = 1;
    ''')

    conn.commit()
    cursor.close()
    conn.close()
