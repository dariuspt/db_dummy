from sqlalchemy import select, update, delete  # Import SQLAlchemy functions for database operations
from .models import products  # Import the products model for database interactions
from .schemas import ProductCreate, ProductUpdate  # Import the schemas for product creation and update validation
from .database import database  # Import the database connection

async def create_product(product: ProductCreate):
    """
    Create a new product in the database.

    Args:
        product (ProductCreate): The product data to create.

    Returns:
        dict: The created product data with its ID.
    """
    query = products.insert().values(**product.dict())  # Prepare insert query with product data
    last_record_id = await database.execute(query)  # Execute the insert query and get the last record ID
    return {**product.dict(), "id": last_record_id}  # Return the created product with ID


async def get_all_products():
    """
    Retrieve all products from the database.

    Returns:
        List[dict]: A list of products.
    """
    query = select(products)  # Prepare query to select all products
    products_list = await database.fetch_all(query)  # Fetch all products from the database
    return [dict(product) for product in products_list]  # Convert each product to a dictionary


async def get_product(product_id: int):
    """
    Retrieve a single product by its ID.

    Args:
        product_id (int): The ID of the product to retrieve.

    Returns:
        dict: The product data if found, None otherwise.
    """
    query = products.select().where(products.c.id == product_id)  # Query to get product by ID
    product = await database.fetch_one(query)  # Fetch the single product from the database
    return dict(product) if product else None  # Convert to dict if found, return None if not


async def update_product(product_id: int, product: ProductUpdate):
    """
    Update an existing product by its ID.

    Args:
        product_id (int): The ID of the product to update.
        product (ProductUpdate): The updated product data.

    Returns:
        dict: The updated product data if successful, None if not found.
    """
    query = products.update().where(products.c.id == product_id).values(**product.dict())  # Prepare update query
    result = await database.execute(query)  # Execute the update query
    if result == 0:  # Check if no rows were affected (product not found)
        return None  # Indicate that the product was not found
    return {**product.dict(), "id": product_id}  # Return the updated product with ID


async def delete_product_and_reassign_ids(product_id: int):
    """
    Delete a product by its ID and reassign IDs for all remaining products.

    Args:
        product_id (int): The ID of the product to delete.

    Returns:
        bool: True if the product was successfully deleted and IDs were reassigned, False otherwise.
    """
    # Delete the specified product from the database
    query = products.delete().where(products.c.id == product_id)  # Prepare delete query
    await database.execute(query)  # Execute the delete query

    # Reassign IDs for remaining products in the database
    query_select = select(products).order_by(products.c.id)  # Prepare query to select all remaining products, ordered by ID
    remaining_products = await database.fetch_all(query_select)  # Fetch all remaining products

    # Reassign IDs starting from 1 for all remaining products
    for new_id, product in enumerate(remaining_products, start=1):  # Enumerate starting from 1
        update_query = (
            update(products)
            .where(products.c.id == product.id)  # Prepare update query for current product
            .values(id=new_id)  # Assign new ID to the product
        )
        await database.execute(update_query)  # Execute the update query

    return True  # Successfully deleted and IDs reassigned


async def delete_product(product_id: int):
    """
    Delete a product by its ID.

    Args:
        product_id (int): The ID of the product to delete.

    Returns:
        bool: True if the product was successfully deleted, False if not found.
    """
    try:
        return await delete_product_and_reassign_ids(product_id)  # Attempt to delete the product and reassign IDs
    except Exception:
        return False  # Handle exceptions gracefully and return False
