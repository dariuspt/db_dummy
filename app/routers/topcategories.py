from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud
from ..database import get_db
import cloudinary.uploader

router = APIRouter()

@router.post("/", response_model=schemas.TopCategory)
async def create_top_category(
    name: str = Form(...),
    description: str = Form(None),
    image: UploadFile = File(None),  # Optional image file for Cloudinary upload
    db: AsyncSession = Depends(get_db)
):
    image_url = None  # Default image URL is None

    # If an image is provided, upload it to Cloudinary
    if image:
        try:
            upload_result = cloudinary.uploader.upload(image.file)
            image_url = upload_result.get("secure_url")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Image upload failed: " + str(e))

    # Prepare the top category creation data
    category_data = schemas.TopCategoryCreate(
        name=name,
        description=description
    )

    # Pass the image URL to the top category creation function
    return await crud.create_top_category(db=db, category=category_data, image_url=image_url)

@router.get("/", response_model=List[schemas.TopCategory])
async def read_top_categories(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_top_categories(db=db, skip=skip, limit=limit)

@router.get("/{category_id}", response_model=schemas.TopCategory)
async def read_category_with_products(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await crud.get_top_category_with_products(db=db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.patch("/{category_id}", response_model=schemas.TopCategory)
async def update_top_category(category_id: int, category: schemas.TopCategoryCreate, db: AsyncSession = Depends(get_db)):
    db_category = await crud.update_top_category(db=db, category_id=category_id, category=category)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/{category_id}", response_model=schemas.TopCategory)
async def delete_top_category(category_id: int, db: AsyncSession = Depends(get_db)):
    db_category = await crud.delete_top_category(db=db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category
