from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import schemas, crud
from ..database import get_db
import cloudinary.uploader

router = APIRouter()

# Create a new category (can be a top category or not based on is_top_category flag)
@router.post("/", response_model=schemas.Category)
async def create_category(
    name: str = Form(...),
    description: str = Form(None),
    is_top_category: bool = Form(False),  # Option to make it a top category
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

    # Prepare the category creation data
    category_data = schemas.CategoryCreate(
        name=name,
        description=description,
        is_top_category=is_top_category  # Include the flag here
    )

    # Pass the image URL to the category creation function
    return await crud.create_category(db=db, category=category_data, image_url=image_url)


# Get all categories (both top and non-top categories)
@router.get("/", response_model=List[schemas.Category])
async def read_all_categories(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_categories(db=db)

# Get only top categories (where is_top_category=True)
@router.get("/top", response_model=List[schemas.Category])
async def get_top_categories(db: AsyncSession = Depends(get_db)):
    categories = await crud.get_top_categories(db=db)
    return categories

# Get a category by ID with its associated products
@router.get("/{identifier}", response_model=schemas.Category)
async def get_category(identifier: str, db: AsyncSession = Depends(get_db)):
    if identifier.isdigit():
        # Search by ID if the identifier is a digit
        category = await crud.get_category_by_id(db=db, category_id=int(identifier))
    else:
        # Search by name if it's not a digit
        category = await crud.get_category_by_name(db=db, category_name=identifier)

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.patch("/{category_id}", response_model=schemas.Category)
async def update_category(
    category_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    is_top_category: Optional[bool] = Form(None),
    image: UploadFile = File(None),  # Optional image file for Cloudinary upload
    db: AsyncSession = Depends(get_db)
):
    # Fetch the existing category by ID
    db_category = await crud.get_category_by_id(db=db, category_id=category_id)

    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Upload the new image if provided
    image_url = db_category.image_url  # Keep the existing image URL if not replaced
    if image:
        try:
            upload_result = cloudinary.uploader.upload(image.file)
            image_url = upload_result.get("secure_url")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Image upload failed: " + str(e))

    # Prepare the data to update
    update_data = {}

    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
    if is_top_category is not None:
        update_data["is_top_category"] = is_top_category

    # Add the new image URL to the update data
    update_data["image_url"] = image_url

    # Call the CRUD function to update the category
    updated_category = await crud.update_category(db=db, category=db_category, updates=update_data)

    return updated_category



# Delete a category by ID (both top and non-top)
@router.delete("/{category_id}", response_model=schemas.Category)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    db_category = await crud.delete_category(db=db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


# Get all SubCategories for a Category
@router.get("/{category_id}/subcategories", response_model=List[schemas.SubCategory])
async def get_subcategories(category_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_subcategories(db=db, category_id=category_id)

