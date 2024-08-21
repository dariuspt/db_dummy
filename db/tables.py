# db/tables.py

from db.connection import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Define table creation SQL commands
    tables = [
        '''
        CREATE TABLE IF NOT EXISTS Categories (
            CategoryID INT PRIMARY KEY,
            CategoryName VARCHAR(255) NOT NULL
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS Suppliers (
            SupplierID INT PRIMARY KEY,
            SupplierName VARCHAR(255) NOT NULL,
            ContactName VARCHAR(255),
            ContactEmail VARCHAR(255)
        );
        ''',
        # Add other table definitions here
    ]

    for table in tables:
        cursor.execute(table)

    conn.commit()
    cursor.close()
    conn.close()
