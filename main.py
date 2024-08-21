import sys
from scripts.create_tables import create_tables
from scripts.insert_data import insert_data
from scripts.query_data import query_data
from scripts.update_delete import update_data, delete_data


def display_help():
    print("Usage:")
    print("  python main.py create_tables   - Create all database tables")
    print("  python main.py insert_data     - Insert sample data into the database")
    print("  python main.py query_data      - Query and display data from the database")
    print("  python main.py update_data     - Update existing data in the database")
    print("  python main.py delete_data     - Delete data from the database")


def main():
    if len(sys.argv) != 2:
        display_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "create_tables":
        create_tables()
    elif command == "insert_data":
        insert_data()
    elif command == "query_data":
        query_data()
    elif command == "update_data":
        update_data()
    elif command == "delete_data":
        delete_data()
    else:
        display_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
