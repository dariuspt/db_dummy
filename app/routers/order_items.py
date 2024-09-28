from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.database import get_session

# Create an APIRouter instance for order-item-related routes
router = APIRouter()

@router.post("/", response_model=schemas.OrderItem)
async def add_item_to_basket(order_item_data: schemas.OrderItemCreate, session: AsyncSession = Depends(get_session)):
    """
    Add an item to the basket (order items), or increase the quantity if it already exists.

    Args:
        order_item_data (schemas.OrderItemCreate): The order item data (product ID, quantity).

    Returns:
        schemas.OrderItem: The created or updated order item data.
    """
    try:
        # Check if the item already exists in the basket
        existing_item = await crud.get_order_item_by_product(order_item_data.order_id, order_item_data.product_id)
        if existing_item:
            # If it exists, update the quantity
            updated_item = await crud.update_order_item_quantity(existing_item.id, order_item_data)
            return updated_item

        # If not, create a new order item
        new_order_item = await crud.add_item_to_order(order_item_data.order_id, order_item_data)
        return new_order_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{order_item_id}", response_model=schemas.OrderItem)
async def fetch_order_item(order_item_id: int, session: AsyncSession = Depends(get_session)):
    """
    Retrieve a specific order item by its ID.

    Args:
        order_item_id (int): The ID of the order item to retrieve.

    Returns:
        schemas.OrderItem: The order item data.
    """
    order_item = await crud.get_order_item_by_id(order_item_id)
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return order_item


@router.get("/order/{order_id}", response_model=list[schemas.OrderItem])
async def fetch_items_in_basket(order_id: int, session: AsyncSession = Depends(get_session)):
    """
    Retrieve all items in the user's basket (order items) for a specific order.

    Args:
        order_id (int): The ID of the order to fetch its items.

    Returns:
        list[schemas.OrderItem]: A list of order items associated with the order.
    """
    order_items = await crud.get_order_items_by_order(order_id)
    if not order_items:
        raise HTTPException(status_code=404, detail="No items found in the basket for this order")
    return order_items


@router.put("/{order_item_id}", response_model=schemas.OrderItem)
async def modify_item_quantity(order_item_id: int, order_item_update: schemas.OrderItemUpdate, session: AsyncSession = Depends(get_session)):
    """
    Update the quantity of an existing item in the basket.

    Args:
        order_item_id (int): The ID of the order item to update.
        order_item_update (schemas.OrderItemUpdate): The updated order item data (e.g., updated quantity).

    Returns:
        schemas.OrderItem: The updated order item data.
    """
    try:
        updated_order_item = await crud.update_order_item_quantity(order_item_id, order_item_update)
        if not updated_order_item:
            raise HTTPException(status_code=404, detail="Order item not found")
        return updated_order_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_item_id}", response_model=dict)
async def remove_item_from_basket(order_item_id: int, session: AsyncSession = Depends(get_session)):
    """
    Remove an item from the basket by its ID.

    Args:
        order_item_id (int): The ID of the order item to remove.

    Returns:
        dict: A message confirming the item was removed from the basket.
    """
    success = await crud.delete_order_item(order_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order item not found")
    return {"detail": "Item removed from the basket"}


@router.post("/confirm-order/{order_id}", response_model=dict)
async def confirm_order(order_id: int, session: AsyncSession = Depends(get_session)):
    """
    Confirm the order, reducing stock from the products table and finalizing the order.

    Args:
        order_id (int): The ID of the order to confirm.

    Returns:
        dict: A success message indicating the order was confirmed and stock was updated.
    """
    try:
        success = await crud.confirm_order(order_id)
        if not success:
            raise HTTPException(status_code=400, detail="Order confirmation failed")
        return {"detail": "Order confirmed, stock updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
