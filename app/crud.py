import cloudinary.uploader
from sqlalchemy import select, update, delete
from .models import Product, Order, OrderItem  # Import the Product, Order, and OrderItem models
from .schemas import ProductCreate, ProductUpdate, OrderCreate, OrderItemCreate, OrderItemUpdate  # Import schemas for data validation
from .database import database  # Import the async database connection
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException


# --- Product Management ---

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
async def update_product(product_id: int, product_data: dict):
    """
    Update an existing product by its ID with the provided data.
    """
    try:
        if not product_data:
            return None  # No data to update

        # Prepare and execute the update query
        query = Product.__table__.update().where(Product.id == product_id).values(product_data)
        result = await database.execute(query)

        if result == 0:
            return None  # Product not found

        return {**product_data, "id": product_id}  # Return updated product data

    except SQLAlchemyError as e:
        print(f"Error updating product {product_id}: {str(e)}")
        raise Exception("Database error occurred while updating the product.")

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
    result = await database.execute(query)  # Execute the delete query
    if result == 0:  # Check if any rows were affected (product not found)
        return False  # Indicate that the product was not found
    return True  # Product successfully deleted


# --- Order Management ---

# Get order item by order ID and product ID
async def get_order_item_by_product(order_id: int, product_id: int):
    """
    Retrieve an order item by its order ID and product ID.

    Args:
        order_id (int): The ID of the order.
        product_id (int): The ID of the product.

    Returns:
        dict: The order item if found, None otherwise.
    """
    query = select(OrderItem).where(OrderItem.order_id == order_id, OrderItem.product_id == product_id)  # Check for existing order item
    return await database.fetch_one(query)  # Return the order item if it exists

# Create a new order
async def create_order(order: OrderCreate):
    """
    Create a new order in the database.

    Args:
        order (OrderCreate): The order data to create.

    Returns:
        dict: The created order with its ID.
    """
    query = Order.__table__.insert().values()  # Insert empty order (default values)
    order_id = await database.execute(query)  # Create the order and get the order ID
    for item in order.order_items:
        await add_item_to_order(order_id, item)  # Add each item in the order
    return {"id": order_id}

# Add an item to an order or increase its quantity
async def add_item_to_order(order_id: int, item: OrderItemCreate):
    """
    Add a new item to an order or increase its quantity if it already exists.

    Args:
        order_id (int): The ID of the order.
        item (OrderItemCreate): The order item to add.

    Returns:
        dict: The created or updated order item.
    """
    try:
        # Check if the item already exists in the order
        query = select(OrderItem).where(OrderItem.order_id == order_id, OrderItem.product_id == item.product_id)
        existing_item = await database.fetch_one(query)

        if existing_item:
            # If it exists, increase the quantity
            new_quantity = existing_item["quantity"] + item.quantity
            await database.execute(
                update(OrderItem)
                .where(OrderItem.id == existing_item["id"])
                .values(quantity=new_quantity)
            )
            return {"detail": f"Quantity updated to {new_quantity} for product {item.product_id}"}

        # If not, create a new order item
        order_item_query = OrderItem.__table__.insert().values(
            order_id=order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            product_name=item.product_name,
            product_price=item.product_price,
        )
        await database.execute(order_item_query)  # Insert the new order item
        return item
    except Exception as e:
        print(f"Error adding item to order: {str(e)}")
        raise ValueError("Failed to add item to order.")

# Update an order item quantity
async def update_order_item_quantity(order_item_id: int, order_item_update: OrderItemUpdate):
    """
    Update the quantity of an item in the order.

    Args:
        order_item_id (int): The ID of the order item to update.
        order_item_update (OrderItemUpdate): The new quantity to update.

    Returns:
        dict: The updated order item data.
    """
    try:
        query = select(OrderItem).where(OrderItem.id == order_item_id)  # Get the specific order item
        order_item = await database.fetch_one(query)

        if not order_item:
            raise ValueError("Order item not found.")  # Raise error if the item doesn't exist

        # Update the quantity of the order item
        await database.execute(
            update(OrderItem)
            .where(OrderItem.id == order_item_id)
            .values(quantity=order_item_update.quantity)
        )
        return {"detail": f"Quantity updated to {order_item_update.quantity}"}
    except Exception as e:
        print(f"Error updating order item quantity: {str(e)}")
        raise ValueError("Failed to update order item quantity.")

# Confirm an order and adjust the stock levels
async def confirm_order(order_id: int):
    """
    Confirm the order, reducing stock levels in the products table.

    Args:
        order_id (int): The ID of the order to confirm.

    Returns:
        dict: Confirmation message indicating stock has been updated.
    """
    try:
        # Get all the items in the order
        order_items_query = select(OrderItem).where(OrderItem.order_id == order_id)
        order_items = await database.fetch_all(order_items_query)

        if not order_items:
            raise ValueError("No items found in the order.")

        # Adjust stock for each product in the order
        for item in order_items:
            product_query = select(Product).where(Product.id == item["product_id"])
            product = await database.fetch_one(product_query)

            if product and product["stock"] >= item["quantity"]:
                new_stock = product["stock"] - item["quantity"]
                await database.execute(
                    update(Product).where(Product.id == item["product_id"]).values(stock=new_stock)
                )
            else:
                raise ValueError(f"Insufficient stock for product {item['product_name']}.")

        return {"detail": "Order confirmed, stock updated"}
    except Exception as e:
        print(f"Error confirming order: {str(e)}")
        raise ValueError("Failed to confirm order.")

# Delete an order item
async def delete_order_item(order_item_id: int):
    """
    Delete an order item by its ID.

    Args:
        order_item_id (int): The ID of the order item to delete.

    Returns:
        bool: True if the order item was successfully deleted.
    """
    try:
        query = select(OrderItem).where(OrderItem.id == order_item_id)
        order_item = await database.fetch_one(query)

        if not order_item:
            raise ValueError("Order item not found.")

        await database.execute(delete(OrderItem).where(OrderItem.id == order_item_id))
        return {"detail": "Order item deleted successfully"}
    except Exception as e:
        print(f"Error deleting order item: {str(e)}")
        raise ValueError("Failed to delete order item.")
