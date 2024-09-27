from fastapi import APIRouter, HTTPException, Depends, UploadFile, File  # Import necessary FastAPI classes
import cloudinary.uploader  # Cloudinary for image uploads
from sqlalchemy.orm import Session
from .. import crud, schemas  # Import CRUD operations and Pydantic schemas
from ..database import get_db  # Import the database session dependency

router = APIRouter()  # Create a new router instance

# Create a new product with optional image upload
@router.post("/", response_model=schemas.Product)
async def create_product(
    product: schemas.ProductCreate,
    image: UploadFile = File(None),  # Optional image file for Cloudinary upload
    db: Session = Depends(get_db)
):
    """
    Create a new product, and optionally upload an image to Cloudinary.

    Args:
        product (ProductCreate): The product data to create.
        image (UploadFile): Optional image file for product image.
        db: Database session dependency.

    Returns:
        Product: The created product data.
    """
    image_url = None  # Default image URL is None

    # If an image is provided, upload it to Cloudinary
    if image:
        try:
            upload_result = cloudinary.uploader.upload(image.file)
            image_url = upload_result.get("secure_url")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Image upload failed: " + str(e))

    # Pass the image URL to the product creation function
    return await crud.create_product(product=product, image_url=image_url)

# Get a product by ID
@router.get("/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a product by its ID.

    Args:
        product_id (int): The ID of the product to retrieve.
        db: Database session dependency.

    Returns:
        Product: The product data.
    """
    product = crud.get_product(product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Get all products
@router.get("/", response_model=list[schemas.Product])
async def get_products():
    """
    Retrieve all products.

    Returns:
        List[Product]: A list of products.
    """
    return await crud.get_all_products()

# Update a product by ID with optional image upload
@router.put("/{product_id}", response_model=schemas.Product)
async def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    image: UploadFile = File(None),  # Optional image file for Cloudinary upload
    db: Session = Depends(get_db)
):
    """
    Update an existing product by its ID, and optionally upload a new image.

    Args:
        product_id (int): The ID of the product to update.
        product (ProductUpdate): The updated product data.
        image (UploadFile): Optional image file for product image.
        db: Database session dependency.

    Returns:
        Product: The updated product data.
    """
    image_url = None  # Default image URL is None

    # If a new image is provided, upload it to Cloudinary
    if image:
        try:
            upload_result = cloudinary.uploader.upload(image.file)
            image_url = upload_result.get("secure_url")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Image upload failed: " + str(e))

    # Pass the image URL to the update function
    updated_product = await crud.update_product(product_id=product_id, product=product, image_url=image_url)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

# Delete a product by ID
@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product by its ID.

    Args:
        product_id (int): The ID of the product to delete.
        db: Database session dependency.

    Returns:
        dict: Confirmation message.
    """
    success = await crud.delete_product(product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}
