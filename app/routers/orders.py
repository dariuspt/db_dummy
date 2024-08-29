from fastapi import APIRouter, HTTPException
from .. import crud, schemas

# Create an APIRouter instance for order-related routes
router = APIRouter()

# Create a new order
@router.post("/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate):
    """
    Create a new order in the database.

    Args:
        order (schemas.OrderCreate): The order data to create.

    Returns:
        schemas.Order: The created order data, including its ID.
    """
    return await crud.create_order(order)

# Get all orders
@router.get("/", response_model=list[schemas.Order])  # Ensure response is a list of orders
async def get_orders():
    """
    Retrieve all orders from the database.

    Returns:
        list[schemas.Order]: A list of all orders.
    """
    return await crud.get_all_orders()

# Cancel an order by ID
@router.delete("/{order_id}", response_model=dict)
async def cancel_order(order_id: int):
    """
    Cancel an order by its ID.

    Args:
        order_id (int): The ID of the order to cancel.

    Returns:
        dict: A success message indicating the order was canceled.

    Raises:
        HTTPException: If the order is not found.
    """
    success = await crud.cancel_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order canceled"}
