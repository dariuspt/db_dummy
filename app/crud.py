import cloudinary.uploader
from sqlalchemy import select, update, delete
from .models import Product, Order, OrderItem  # Import the Product, Order, and OrderItem models
from .schemas import ProductCreate, ProductUpdate, OrderCreate, OrderItemCreate, OrderItemUpdate  # Import schemas for data validation
from .database import database  # Import the async database connection
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError


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
    try:
        # Prepare product data for update, excluding unset fields
        product_data = product.dict(exclude_unset=True)

        # If an image_url is provided, update the image_url field
        if image_url:
            product_data["image_url"] = image_url

        # Prepare and execute the update query
        query = Product.__table__.update().where(Product.id == product_id).values(product_data)
        result = await database.execute(query)

        # Check if any rows were affected (i.e., if the product was found and updated)
        if result == 0:
            return None  # Product not found

        # Return the updated product data, including the product ID
        return {**product_data, "id": product_id}

    except SQLAlchemyError as e:
        # Catch and log any database-related errors
        print(f"Error updating product {product_id}: {str(e)}")
        raise Exception("Database error occurred while updating the product.")

    except Exception as e:
        # Catch any other errors that might occur
        print(f"Unexpected error occurred while updating product {product_id}: {str(e)}")
        raise Exception("An unexpected error occurred while updating the product.")


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


# --- Order Management ---

# Create a new order
async def create_order(order: OrderCreate):
    """
    Create a new order in the database.

    Args:
        order (OrderCreate): The order data to create.

    Returns:
        dict: The created order with its ID.
    """
    query = Order.__table__.insert().values()  # Insert empty order (use default values)
    order_id = await database.execute(query)

    # Add each item in the order to the order_items table
    for item in order.order_items:
        await add_item_to_order(order_id, item)

    return {"id": order_id}


# Add an item to an order (e.g., the basket)
async def add_item_to_order(order_id: int, item: OrderItemCreate):
    """
    Add a new item to an order.

    Args:
        order_id (int): The ID of the order.
        item (OrderItemCreate): The order item to add.

    Returns:
        None
    """
    # Fetch the product to check availability and stock
    product_query = select(Product).where(Product.id == item.product_id)
    product = await database.fetch_one(product_query)

    if product is None or product["stock"] < item.quantity:
        raise ValueError("Product not available or insufficient stock.")

    # Insert the order item into the order_items table
    order_item_query = OrderItem.__table__.insert().values(
        order_id=order_id,
        product_id=item.product_id,
        quantity=item.quantity,
        product_name=product["name"],
        product_price=product["price"],
    )
    await database.execute(order_item_query)


# Update an order item quantity in the basket
async def update_order_item_quantity(order_item_id: int, order_item_update: OrderItemUpdate):
    """
    Update the quantity of an item in the order (e.g., basket).

    Args:
        order_item_id (int): The ID of the order item to update.
        order_item_update (OrderItemUpdate): The new quantity to update.

    Returns:
        dict: The updated order item data.
    """
    query = OrderItem.__table__.update().where(OrderItem.id == order_item_id).values(
        quantity=order_item_update.quantity
    )
    result = await database.execute(query)

    if result == 0:
        return None  # Item not found

    return result


# Confirm an order and adjust the stock levels
async def confirm_order(order_id: int):
    """
    Confirm the order, reducing stock levels in the products table.

    Args:
        order_id (int): The ID of the order to confirm.

    Returns:
        dict: Confirmation message indicating stock has been updated.
    """
    # Retrieve all the items in the order
    order_items_query = select(OrderItem).where(OrderItem.order_id == order_id)
    order_items = await database.fetch_all(order_items_query)

    # Adjust stock for each product in the order
    for item in order_items:
        product_query = select(Product).where(Product.id == item.product_id)
        product = await database.fetch_one(product_query)

        if product and product["stock"] >= item["quantity"]:
            new_stock = product["stock"] - item["quantity"]
            update_stock_query = Product.__table__.update().where(Product.id == item.product_id).values(stock=new_stock)
            await database.execute(update_stock_query)
        else:
            raise ValueError("Insufficient stock to fulfill the order.")

    return {"detail": "Order confirmed and stock updated"}


# Delete an order item (e.g., removing from basket)
async def delete_order_item(order_item_id: int):
    """
    Delete an order item by its ID.

    Args:
        order_item_id (int): The ID of the order item to delete.

    Returns:
        bool: True if the order item was successfully deleted.
    """
    query = OrderItem.__table__.delete().where(OrderItem.id == order_item_id)
    result = await database.execute(query)
    return result > 0
