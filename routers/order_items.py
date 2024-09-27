from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.database import get_session

# Create an APIRouter instance for order-item-related routes
router = APIRouter()

@router.post("/", response_model=schemas.OrderItem)
async def create_order_item(order_item: schemas.OrderItemCreate, session: AsyncSession = Depends(get_session)):
    """
    Create a new order item in the database.

    Args:
        order_item (schemas.OrderItemCreate): The order item data to create.

    Returns:
        schemas.OrderItem: The created order item data, including its ID.
    """
    try:
        return await crud.create_order_item(session, order_item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{order_item_id}", response_model=schemas.OrderItem)
async def get_order_item(order_item_id: int, session: AsyncSession = Depends(get_session)):
    """
    Retrieve a specific order item by its ID.

    Args:
        order_item_id (int): The ID of the order item to retrieve.

    Returns:
        schemas.OrderItem: The order item data.
    """
    order_item = await crud.get_order_item(session, order_item_id)
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return order_item

@router.get("/order/{order_id}", response_model=list[schemas.OrderItem])
async def get_order_items(order_id: int, session: AsyncSession = Depends(get_session)):
    """
    Retrieve all order items for a specific order.

    Args:
        order_id (int): The ID of the order whose items are to be retrieved.

    Returns:
        list[schemas.OrderItem]: A list of all order items for the specified order.
    """
    order_items = await crud.get_order_items(session, order_id)
    if not order_items:
        raise HTTPException(status_code=404, detail="No order items found for this order")
    return order_items

@router.put("/{order_item_id}", response_model=schemas.OrderItem)
async def update_order_item(order_item_id: int, order_item_update: schemas.OrderItemUpdate, session: AsyncSession = Depends(get_session)):
    """
    Update an existing order item by its ID.

    Args:
        order_item_id (int): The ID of the order item to update.
        order_item_update (schemas.OrderItemUpdate): The updated order item data.

    Returns:
        schemas.OrderItem: The updated order item data.
    """
    try:
        updated_item = await crud.update_order_item(session, order_item_id, order_item_update)
        if not updated_item:
            raise HTTPException(status_code=404, detail="Order item not found")
        return updated_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{order_item_id}", response_model=dict)
async def delete_order_item(order_item_id: int, session: AsyncSession = Depends(get_session)):
    """
    Delete an order item by its ID.

    Args:
        order_item_id (int): The ID of the order item to delete.

    Returns:
        dict: A success message indicating the order item was deleted.
    """
    success = await crud.delete_order_item(session, order_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order item not found")
    return {"detail": "Order item deleted"}
