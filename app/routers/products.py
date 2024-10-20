from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud
from ..database import get_db
import cloudinary.uploader
from ..crud import get_product_with_category
from sqlalchemy.future import select
from .. import models

router = APIRouter()

@router.post("/", response_model=schemas.Product)
async def create_product(
    name: str = Form(...),
    producer: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    stock: int = Form(...),
    category: str = Form(...),  # Pass category name
    subcategory: str = Form(...),
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

    # Lookup category_id based on category name
    result = await db.execute(select(models.TopCategory).where(models.TopCategory.name == category))
    category_instance = result.scalars().first()

    if not category_instance:
        raise HTTPException(status_code=404, detail="Category not found")

    # Prepare the product creation data
    product_data = schemas.ProductCreate(
        name=name,
        producer=producer,
        description=description,
        price=price,
        stock=stock,
        category_id=category_instance.id,  # Use the resolved category_id
        subcategory=subcategory
    )

    # Pass the image URL to the product creation function
    return await crud.create_product(db=db, product=product_data, image_url=image_url)


@router.get("/", response_model=List[schemas.Product])
async def read_products(db: AsyncSession = Depends(get_db)):
    # Fetch all products without pagination
    try:
        products = await crud.get_all_products(db=db)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=schemas.Product)
async def read_product_with_category(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_product_and_category(db=db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.patch("/{product_id}", response_model=schemas.Product)
async def update_product(
        product_id: int,
        product_data: schemas.ProductUpdate,  # Ensure this is your update schema
        db: AsyncSession = Depends(get_db)
):
    # Fetch the existing product from the database
    product = await crud.get_product_by_id(db=db, product_id=product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Call the update function in CRUD
    return await crud.update_product(db=db, product=product, updates=product_data)

@router.delete("/{product_id}", response_model=schemas.Product)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    db_product = await crud.delete_product(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

async def get_product_and_category(db: AsyncSession, product_id: int):
    return await get_product_with_category(db, product_id)