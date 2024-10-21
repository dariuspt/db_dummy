from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud
from ..database import get_db

router = APIRouter()


# ================================
# CRUD API for Subcategories
# ================================

# Create a new SubCategory
@router.post("/", response_model=schemas.SubCategory)
async def create_subcategory(subcategory: schemas.SubCategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_subcategory(db=db, subcategory=subcategory)


# Get a specific SubCategory by ID
@router.get("/{subcategory_id}", response_model=schemas.SubCategory)
async def get_subcategory(subcategory_id: int, db: AsyncSession = Depends(get_db)):
    subcategory = await crud.get_subcategory_by_id(db=db, subcategory_id=subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    return subcategory


# Update an existing SubCategory
@router.patch("/{subcategory_id}", response_model=schemas.SubCategory)
async def update_subcategory(subcategory_id: int, subcategory_update: schemas.SubCategoryCreate,
                             db: AsyncSession = Depends(get_db)):
    subcategory = await crud.get_subcategory_by_id(db=db, subcategory_id=subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    updated_subcategory = await crud.update_subcategory(db=db, subcategory=subcategory, updates=subcategory_update)
    return updated_subcategory


# Delete a SubCategory by ID
@router.delete("/{subcategory_id}", response_model=schemas.SubCategory)
async def delete_subcategory(subcategory_id: int, db: AsyncSession = Depends(get_db)):
    subcategory = await crud.delete_subcategory(db=db, subcategory_id=subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    return subcategory
