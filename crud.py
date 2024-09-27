import cloudinary.uploader
from sqlalchemy import select, update, delete
from .models import Product, Order, OrderItem  # Import the Product, Order, and OrderItem models
from .schemas import ProductCreate, ProductUpdate, OrderCreate  # Import schemas for data validation
from .database import database  # Import the async database connection
from sqlalchemy.orm import selectinload


# Create a new product with optional image_url
async def create_product(product: ProductCreate, image_url: str = None):
    """
    Create a new product in the database with optional image_url.

    Args:
        product (ProductCreate): The product data to create.
        image_url (str): The URL of the product image uploaded to Cloudinary.

    Returns:
        dict: The created product data with its ID.
    """
    # Prepare the insert query including the image URL if provided
    query = Product.__table__.insert().values(
        name=product.name,
        producer=product.producer,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category,
        subcategory=product.subcategory,
        image_url=image_url  # Save image URL from Cloudinary
    )

    last_record_id = await database.execute(query)  # Execute the insert query and get the last record ID
    return {**product.dict(), "id": last_record_id, "image_url": image_url}  # Return the created product with ID


# Retrieve all products
async def get_all_products():
    """
    Retrieve all products from the database.

    Returns:
        List[dict]: A list of products.
    """
    query = select(Product)  # Prepare query to select all products
    products_list = await database.fetch_all(query)  # Fetch all products from the database
    return [dict(product) for product in products_list]  # Convert each product to a dictionary


# Retrieve a single product by its ID
async def get_product(product_id: int):
    """
    Retrieve a single product by its ID.

    Args:
        product_id (int): The ID of the product to retrieve.

    Returns:
        dict: The product data if found, None otherwise.
    """
    query = select(Product).where(Product.id == product_id)  # Query to get product by ID
    product = await database.fetch_one(query)  # Fetch the single product from the database
    return dict(product) if product else None  # Convert to dict if found, return None if not


# Update an existing product by its ID with optional image_url
async def update_product(product_id: int, product: ProductUpdate, image_url: str = None):
    """
    Update an existing product by its ID with optional image_url.

    Args:
        product_id (int): The ID of the product to update.
        product (ProductUpdate): The updated product data.
        image_url (str): The new URL of the product image uploaded to Cloudinary.

    Returns:
        dict: The updated product data if successful, None if not found.
    """
    product_data = product.dict(exclude_unset=True)  # Prepare product data for update

    # If an image_url is provided, update the image_url field
    if image_url:
        product_data["image_url"] = image_url

    query = Product.__table__.update().where(Product.id == product_id).values(product_data)  # Prepare update query
    result = await database.execute(query)  # Execute the update query

    if result == 0:  # Check if no rows were affected (product not found)
        return None  # Indicate that the product was not found
    return {**product_data, "id": product_id}  # Return the updated product with ID


# Delete a product by its ID
async def delete_product(product_id: int):
    """
    Delete a product by its ID.

    Args:
        product_id (int): The ID of the product to delete.

    Returns:
        bool: True if the product was successfully deleted, False if not found.
    """
    query = Product.__table__.delete().where(Product.id == product_id)  # Prepare delete query
    result = await database.execute(query)  # Execute the delete
    if result == 0:  # Check if no rows were affected (product not found)
        return False  # Indicate that the product was not found
    return True  # Successfully deleted
