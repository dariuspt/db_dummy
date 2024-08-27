from sqlalchemy import Table, Column, Integer, String, Float, MetaData

# Create a MetaData instance to hold information about the database schema
metadata = MetaData()

# Define the products table with its schema
products = Table(
    "products",  # Name of the table in the database
    metadata,  # Reference to the MetaData instance
    Column("id", Integer, primary_key=True, autoincrement=True),  # ID column as the primary key, auto-incremented
    Column("name", String(100), nullable=False),  # Product name column, required (not nullable), max length 100 characters
    Column("description", String(255)),  # Product description column, optional, max length 255 characters
    Column("price", Float, nullable=False),  # Product price column, required (not nullable), data type is Float
)
