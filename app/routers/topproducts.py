from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.TopProduct)
async def create_top_product(top_product: schemas.TopProductCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_top_product(db=db, top_product=top_product)

@router.get("/", response_model=List[schemas.TopProduct])
async def read_top_products(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_top_products(db=db, skip=skip, limit=limit)

@router.get("/{top_product_id}", response_model=schemas.TopProduct)
async def read_top_product(top_product_id: int, db: AsyncSession = Depends(get_db)):
    db_top_product = await crud.get_top_product_by_id(db=db, top_product_id=top_product_id)
    if not db_top_product:
        raise HTTPException(status_code=404, detail="Top Product not found")
    return db_top_product


@router.patch("/{top_product_id}", response_model=schemas.TopProduct)
async def update_top_product(
        top_product_id: int,
        top_product_data: schemas.TopProductUpdate,  # Update schema
        db: AsyncSession = Depends(get_db)
):
    # Fetch the top product from the database using the provided ID
    top_product = await crud.get_top_product_by_id(db=db, top_product_id=top_product_id)

    if not top_product:
        raise HTTPException(status_code=404, detail="Top Product not found")

    # Call the update function in CRUD
    return await crud.update_top_product(db=db, top_product=top_product, updates=top_product_data)

@router.delete("/{top_product_id}", response_model=schemas.TopProduct)
async def delete_top_product(top_product_id: int, db: AsyncSession = Depends(get_db)):
    db_top_product = await crud.delete_top_product(db=db, top_product_id=top_product_id)
    if not db_top_product:
        raise HTTPException(status_code=404, detail="Top Product not found")
    return db_top_product
