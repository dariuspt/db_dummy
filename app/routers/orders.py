from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud
from ..database import get_db


router = APIRouter()

@router.post("/", response_model=schemas.Order)
async def create_order_endpoint(order_data: schemas.OrderCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_order(db=db, order_data=order_data)

@router.get("/{order_id}", response_model=schemas.Order)
async def get_order_endpoint(order_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_order_by_id(db=db, order_id=order_id)
