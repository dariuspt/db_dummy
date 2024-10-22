from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud
from ..database import get_db
import cloudinary.uploader
from ..crud import get_product_with_category, get_product_by_name ,get_product_by_id
from sqlalchemy.future import select
from .. import models
import re

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
    is_top_product: bool = Form(None),
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
    result = await db.execute(select(models.Category).where(models.Category.name == category))
    category_instance = result.scalars().first()

    result = await db.execute(select(models.SubCategory).where(models.SubCategory.name == subcategory))
    subcategory_instance = result.scalars().first()

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
        is_top_product=is_top_product,
        subcategory_id=subcategory_instance.id
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

@router.get("/top", response_model=List[schemas.Product])
async def get_top_products(db: AsyncSession = Depends(get_db)):
    products = await crud.get_top_products(db=db)
    return products


@router.get("/{identifier}", response_model=schemas.Product)
async def read_product_by_id_or_name(identifier: str, db: AsyncSession = Depends(get_db)):
    # Check if the identifier is numeric, indicating it's an ID
    if re.match(r'^\d+$', identifier):
        product = await get_product_by_id(db=db, product_id=int(identifier))
    else:
        product = await get_product_by_name(db=db, product_name=identifier)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}", response_model=schemas.Product)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    # Fetch the product from the database
    db_product = await crud.get_product_by_id_only_delete(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Proceed to delete if found
    deleted_product = await crud.delete_product(db=db, db_product=db_product)
    return deleted_product

async def get_product_and_category(db: AsyncSession, product_id: int):
    return await get_product_with_category(db, product_id)


# Get products by Category
@router.get("/categories/{category_id}/products", response_model=List[schemas.Product])
async def get_products_by_category(category_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_products_by_category(db=db, category_id=category_id)

# Get products by SubCategory
@router.get("/subcategories/{subcategory_id}/products", response_model=List[schemas.Product])
async def get_products_by_subcategory(subcategory_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_products_by_subcategory(db=db, subcategory_id=subcategory_id)

