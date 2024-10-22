from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union
from .. import schemas, crud, models
from ..database import get_db


router = APIRouter()


# ================================
# CRUD API for Subcategories
# ================================

# Get all subcategories
@router.get("/", response_model=List[schemas.SubCategory])
async def get_all_subcategories(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_subcategories(db=db)


# Create a new SubCategory
@router.post("/", response_model=schemas.SubCategory)
async def create_subcategory(
    name: str = Form(...),
    category_identifier: Union[str, int] = Form(...),  # Accept either ID or name for the category
    db: AsyncSession = Depends(get_db)
):
    # If the category_identifier is an integer, look up the category by ID
    if isinstance(category_identifier, int):
        result = await db.execute(select(models.Category).where(models.Category.id == category_identifier))
        category_instance = result.scalars().first()
    # Otherwise, treat it as a string and look up the category by name
    else:
        result = await db.execute(select(models.Category).where(models.Category.name == category_identifier))
        category_instance = result.scalars().first()

    # Handle case where the category is not found
    if not category_instance:
        raise HTTPException(status_code=404, detail="Category not found")

    # Create the new subcategory with the resolved category ID
    subcategory_data = schemas.SubCategoryCreate(
        name=name,
        category_identifier=category_instance.id  # We resolve the identifier to category ID
    )

    # Call CRUD function to create the subcategory
    return await crud.create_subcategory(db=db, subcategory=subcategory_data)


# Get a specific SubCategory by ID
@router.get("/{identifier}", response_model=schemas.SubCategory)
async def get_subcategory(identifier: str, db: AsyncSession = Depends(get_db)):
    if identifier.isdigit():
        # Search by ID if the identifier is a digit
        subcategory = await crud.get_subcategory_by_id(db=db, subcategory_id=int(identifier))
    else:
        # Search by name if it's not a digit
        subcategory = await crud.get_subcategory_by_name(db=db, subcategory_name=identifier)

    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    return subcategory


# Update an existing SubCategory
@router.patch("/{subcategory_id}", response_model=schemas.SubCategory)
async def update_subcategory(
        subcategory_id: int,
        subcategory_update: schemas.SubCategoryUpdate,  # This expects JSON payload, hence using it as a pydantic schema
        db: AsyncSession = Depends(get_db)
):
    # Fetch the existing subcategory by ID
    subcategory = await crud.get_subcategory_by_id(db=db, subcategory_id=subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    # Pass to CRUD function to handle the update
    updated_subcategory = await crud.update_subcategory(
        db=db,
        subcategory=subcategory,
        updates=subcategory_update
    )

    if not updated_subcategory:
        raise HTTPException(status_code=500, detail="Failed to update subcategory")

    return updated_subcategory


# Delete a SubCategory by ID
@router.delete("/{subcategory_id}", response_model=schemas.SubCategory)
async def delete_subcategory(subcategory_id: int, db: AsyncSession = Depends(get_db)):
    subcategory = await crud.delete_subcategory(db=db, subcategory_id=subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    return subcategory
