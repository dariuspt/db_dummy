from sqlalchemy import create_engine, MetaData  # Import necessary functions from SQLAlchemy
from databases import Database  # Import the Database class for async database operations
from .config import DATABASE_URL  # Import the database URL from the config module

# Create an instance of the Database class for asynchronous operations
database = Database(DATABASE_URL)

# Create a MetaData instance to hold information about the database schema
metadata = MetaData()

# Create a SQLAlchemy engine instance for synchronous database operations
engine = create_engine(DATABASE_URL)  # This will be used for creating sessions or running migrations
