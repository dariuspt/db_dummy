from dotenv import load_dotenv
import os
import mysql.connector

# Load environment variables from .env file
load_dotenv()

# Get database configuration from environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
}

# Connect to the database
try:
    connection = mysql.connector.connect(**db_config)
    print("Database connection successful!")

    # Your database operations here

finally:
    if connection.is_connected():
        connection.close()
        print("Database connection closed.")
