from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union, Optional
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
    name: Optional[str] = Form(None),  # Accept subcategory name
    category: Optional[str] = Form(None),  # Optional category name
    db: AsyncSession = Depends(get_db)
):
    # Fetch the existing subcategory by ID (this should return a model instance)
    db_subcategory = await crud.get_subcategory_by_id_for_update(db=db, subcategory_id=subcategory_id)

    if not db_subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    # Prepare the data to update
    update_data = {}

    if name is not None:
        update_data["name"] = name

    # If category name is provided, resolve the category ID
    if category is not None:
        result = await db.execute(select(models.Category).where(models.Category.name == category))
        category_instance = result.scalars().first()
        if not category_instance:
            raise HTTPException(status_code=404, detail="Category not found")
        update_data["category_id"] = category_instance.id

    # Call the CRUD function to update the subcategory
    updated_subcategory = await crud.update_subcategory(db=db, subcategory=db_subcategory, updates=update_data)

    return updated_subcategory


# Delete a SubCategory by ID
@router.delete("/{subcategory_id}", response_model=schemas.SubCategory)
async def delete_subcategory(subcategory_id: int, db: AsyncSession = Depends(get_db)):
    subcategory = await crud.delete_subcategory(db=db, subcategory_id=subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    return subcategory
