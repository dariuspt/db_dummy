from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud
from ..database import get_db


router = APIRouter()


@router.get("/", response_model=List[schemas.Order])
async def get_all_orders_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_orders(db)


@router.post("/", response_model=schemas.Order)
async def create_order_endpoint(order_data: schemas.OrderCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_order(db, order_data)
    except Exception as e:
        # Log the error for better debugging
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{order_id}", response_model=schemas.Order)
async def get_order_by_id_endpoint(order_id: int, db: AsyncSession = Depends(get_db)):
    """
    Endpoint to get an order by its ID.
    """
    order = await crud.get_order_by_id(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
