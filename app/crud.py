from sqlalchemy import select, update, delete
from .models import Product, Order, OrderItem
from .schemas import ProductCreate, ProductUpdate, OrderCreate, OrderItemCreate, OrderItemUpdate
from .database import database
from sqlalchemy.exc import SQLAlchemyError


# Add item to basket or increase the quantity if it already exists
async def get_order_item_by_product(session, order_id: int, product_id: int):
    """
    Retrieve an order item by product and order ID if it exists.

    Args:
        session: The database session.
        order_id (int): The ID of the order.
        product_id (int): The ID of the product.

    Returns:
        OrderItem: The order item if found, else None.
    """
    query = select(OrderItem).where(OrderItem.order_id == order_id, OrderItem.product_id == product_id)
    return await session.execute(query).scalars().first()

async def add_item_to_order(session, order_item_data: OrderItemCreate):
    """
    Add a new item to the order.

    Args:
        session: The database session.
        order_item_data: The order item data (product ID, quantity).

    Returns:
        OrderItem: The newly created order item.
    """
    product = await session.execute(select(Product).where(Product.id == order_item_data.product_id)).scalars().first()

    if product is None or product.stock < order_item_data.quantity:
        raise ValueError("Product not available or insufficient stock.")

    new_order_item = OrderItem(
        order_id=order_item_data.order_id,
        product_id=order_item_data.product_id,
        quantity=order_item_data.quantity,
        product_name=product.name,
        product_price=product.price
    )
    session.add(new_order_item)
    await session.commit()
    return new_order_item

# Increase the quantity of an existing item
async def increase_item_quantity(session, order_item_id: int, additional_quantity: int):
    """
    Increase the quantity of an existing order item in the basket.

    Args:
        session: The database session.
        order_item_id (int): The ID of the order item to update.
        additional_quantity (int): The quantity to add.

    Returns:
        OrderItem: The updated order item.
    """
    query = update(OrderItem).where(OrderItem.id == order_item_id).values(
        quantity=OrderItem.quantity + additional_quantity)
    await session.execute(query)
    await session.commit()

    # Fetch the updated order item
    return await session.execute(select(OrderItem).where(OrderItem.id == order_item_id)).scalars().first()

# Fetch an order item by ID
async def fetch_order_item_by_id(session, order_item_id: int):
    """
    Retrieve an order item by its ID.

    Args:
        session: The database session.
        order_item_id (int): The ID of the order item.

    Returns:
        OrderItem: The order item if found, else None.
    """
    return await session.execute(select(OrderItem).where(OrderItem.id == order_item_id)).scalars().first()

# Fetch all items by order ID
async def fetch_items_by_order_id(session, order_id: int):
    """
    Retrieve all order items for a specific order.

    Args:
        session: The database session.
        order_id (int): The ID of the order.

    Returns:
        list[OrderItem]: A list of order items.
    """
    return await session.execute(select(OrderItem).where(OrderItem.order_id == order_id)).scalars().all()

# Update order item quantity
async def modify_order_item_quantity(session, order_item_id: int, order_item_update: OrderItemUpdate):
    """
    Modify the quantity of an existing order item.

    Args:
        session: The database session.
        order_item_id (int): The ID of the order item to update.
        order_item_update (OrderItemUpdate): The new quantity to update.

    Returns:
        OrderItem: The updated order item.
    """
    query = update(OrderItem).where(OrderItem.id == order_item_id).values(
        quantity=order_item_update.quantity
    )
    await session.execute(query)
    await session.commit()

    return await session.execute(select(OrderItem).where(OrderItem.id == order_item_id)).scalars().first()

# Delete an order item by ID
async def remove_item_from_order(session, order_item_id: int):
    """
    Delete an order item from the basket.

    Args:
        session: The database session.
        order_item_id (int): The ID of the order item to delete.

    Returns:
        bool: True if the item was successfully deleted, False otherwise.
    """
    query = delete(OrderItem).where(OrderItem.id == order_item_id)
    result = await session.execute(query)
    await session.commit()
    return result.rowcount > 0

# Confirm an order and reduce product stock
async def confirm_order(session, order_id: int):
    """
    Confirm the order and reduce stock levels in the products table.

    Args:
        session: The database session.
        order_id (int): The ID of the order to confirm.

    Returns:
        dict: Confirmation message indicating stock has been updated.
    """
    order_items = await session.execute(select(OrderItem).where(OrderItem.order_id == order_id)).scalars().all()

    if not order_items:
        return False

    for item in order_items:
        product = await session.execute(select(Product).where(Product.id == item.product_id)).scalars().first()

        if product.stock < item.quantity:
            raise ValueError(f"Insufficient stock for product {product.name}")

        # Reduce product stock
        new_stock = product.stock - item.quantity
        await session.execute(update(Product).where(Product.id == product.id).values(stock=new_stock))

    await session.commit()
    return True
