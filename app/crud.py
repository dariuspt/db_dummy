from sqlalchemy import select, update, delete
from .models import Product  # Import the Product model
from .schemas import ProductCreate, ProductUpdate, OrderCreate, Order, OrderItem  # Import schemas for data validation
from .database import database  # Import the async database connection
from sqlalchemy.orm import selectinload

async def create_product(product: ProductCreate):
    """
    Create a new product in the database.

    Args:
        product (ProductCreate): The product data to create.

    Returns:
        dict: The created product data with its ID.
    """
    query = Product.__table__.insert().values(**product.dict())  # Prepare the insert query
    last_record_id = await database.execute(query)  # Execute the insert query and get the last record ID
    return {**product.dict(), "id": last_record_id}  # Return the created product with ID

async def get_all_products():
    """
    Retrieve all products from the database.

    Returns:
        List[dict]: A list of products.
    """
    query = select(Product)  # Prepare query to select all products
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
    query = select(Product).where(Product.id == product_id)  # Query to get product by ID
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
    query = Product.__table__.update().where(Product.id == product_id).values(**product.dict())  # Prepare update query
    result = await database.execute(query)  # Execute the update query
    if result == 0:  # Check if no rows were affected (product not found)
        return None  # Indicate that the product was not found
    return {**product.dict(), "id": product_id}  # Return the updated product with ID

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


async def create_order(order_data: OrderCreate):
    # Step 1: Create the Order
    new_order = Order()
    database.add(new_order)
    await database.commit()
    await database.refresh(new_order)

    # Step 2: Create OrderItems and associate them with the Order
    order_items = []
    for item in order_data.order_items:
        # Fetch the Product to ensure it exists and to update stock
        product = await database.get(Product, item.product_id)
        if product and product.stock >= item.quantity:
            # Reduce the product stock
            product.stock -= item.quantity
            await database.commit()

            # Create an OrderItem
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=item.quantity,
                product_name=product.name,
                product_price=product.price,
            )
            database.add(order_item)
            order_items.append(order_item)
        else:
            raise Exception(f"Not enough stock for product ID: {item.product_id}")

    await database.commit()

    # Return the created order with its items
    return {
        "id": new_order.id,
        "created_at": new_order.created_at,
        "order_items": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "product_name": item.product_name,
                "product_price": item.product_price,
            }
            for item in order_items
        ]
    }


# New function to retrieve all orders
async def get_order(order_id: int):
    query = select(Order).options(selectinload(Order.order_items))
    result = await database.execute(query.where(Order.id == order_id))
    order = result.scalars().first()

    if not order:
        return None

    return {
        "id": order.id,
        "created_at": order.created_at,
        "order_items": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "product_name": item.product_name,
                "product_price": item.product_price,
            }
            for item in order.order_items
        ]
    }


async def update_order_item(order_id: int, product_id: int, new_quantity: int):
    # Fetch the OrderItem
    order_item = await database.get(OrderItem, (order_id, product_id))
    if not order_item:
        return None

    # Adjust the stock of the associated Product
    product = await database.get(Product, product_id)
    if not product:
        return None

    # Update the stock level
    product.stock += order_item.quantity  # Revert the old quantity
    if product.stock < new_quantity:
        raise Exception("Not enough stock to increase quantity")

    product.stock -= new_quantity
    order_item.quantity = new_quantity

    await database.commit()

    return {
        "order_id": order_item.order_id,
        "product_id": order_item.product_id,
        "quantity": order_item.quantity,
        "product_name": order_item.product_name,
        "product_price": order_item.product_price,
    }


# New function to cancel an order
async def cancel_order(order_id: int):
    """
    Cancel an existing order and restore the stock of products.

    Args:
        order_id (int): The ID of the order to cancel.

    Returns:
        bool: True if the order was successfully canceled, False if not found.
    """
    # Retrieve the order items
    order_items_query = select(OrderItem).where(OrderItem.order_id == order_id)
    order_items = await database.fetch_all(order_items_query)

    if not order_items:
        return False  # Order not found

    # Restore stock for each product in the order
    product_updates = []
    for item in order_items:
        product_query = select(Product).where(Product.id == item.product_id)
        product = await database.fetch_one(product_query)

        if product:
            new_stock = product.stock + item.quantity
            product_updates.append({"id": item.product_id, "new_stock": new_stock})

    # Execute all stock updates
    for update in product_updates:
        update_query = (
            Product.__table__.update()
            .where(Product.id == update["id"])
            .values(stock=update["new_stock"])
        )
        await database.execute(update_query)

    # Delete the order items
    delete_items_query = OrderItem.__table__.delete().where(OrderItem.order_id == order_id)
    await database.execute(delete_items_query)

    # Delete the order
    delete_order_query = Order.__table__.delete().where(Order.id == order_id)
    await database.execute(delete_order_query)

    return True  # Successfully canceled the order

