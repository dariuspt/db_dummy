from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_order(db=db, order=order)

@router.get("/", response_model=List[schemas.Order])
async def read_orders(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_orders(db=db, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=schemas.Order)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    db_order = await crud.get_order_by_id(db=db, order_id=order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.patch("/{order_id}", response_model=schemas.Order)
async def update_order(order_id: int, order: schemas.OrderCreate, db: AsyncSession = Depends(get_db)):
    db_order = await crud.update_order(db=db, order_id=order_id, order=order)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.delete("/{order_id}", response_model=schemas.Order)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    db_order = await crud.delete_order(db=db, order_id=order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
