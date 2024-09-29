from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form  # Import necessary FastAPI classes
import cloudinary.uploader  # Cloudinary for image uploads
from sqlalchemy.orm import Session
from .. import crud, schemas  # Import CRUD operations and Pydantic schemas
from ..database import get_db  # Import the database session dependency

router = APIRouter()  # Create a new router instance

# Create a new product with optional image upload
@router.post("/", response_model=schemas.Product)
async def create_product(
    name: str = Form(...),
    producer: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    stock: int = Form(...),
    category: str = Form(...),
    subcategory: str = Form(...),
    image: UploadFile = File(None),  # Optional image file for Cloudinary upload
    db: Session = Depends(get_db)
):
    """
    Create a new product, and optionally upload an image to Cloudinary.

    Args:
        name (str): The product name.
        producer (str): The product producer.
        description (str): The product description (optional).
        price (float): The price of the product.
        stock (int): The stock of the product.
        category (str): The product category.
        subcategory (str): The product subcategory.
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

    # Prepare the product creation data
    product_data = schemas.ProductCreate(
        name=name,
        producer=producer,
        description=description,
        price=price,
        stock=stock,
        category=category,
        subcategory=subcategory
    )

    # Pass the image URL to the product creation function
    return await crud.create_product(product=product_data, image_url=image_url)


# Get a product by ID
@router.get("/{product_id}", response_model=schemas.Product)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a product by its ID.

    Args:
        product_id (int): The ID of the product to retrieve.
        db: Database session dependency.

    Returns:
        Product: The product data.
    """
    try:
        product = await crud.get_product(product_id=product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# Get all products
@router.get("/", response_model=list[schemas.Product])
async def get_products():
    """
    Retrieve all products.

    Returns:
        List[Product]: A list of products.
    """
    return await crud.get_all_products()


@router.put("/{product_id}", response_model=schemas.Product)
async def update_product(
        product_id: int,
        name: str = Form(...),
        producer: str = Form(...),
        description: str = Form(None),
        price: float = Form(...),
        stock: int = Form(...),
        category: str = Form(...),
        subcategory: str = Form(...),
        image: UploadFile = File(None),  # Optional image file for Cloudinary upload
        db: Session = Depends(get_db)
):
    """
    Update an existing product by its ID, and optionally upload a new image.

    Args:
        product_id (int): The ID of the product to update.
        name (str): The updated product name.
        producer (str): The updated product producer.
        description (str): The updated product description (optional).
        price (float): The updated price of the product.
        stock (int): The updated stock of the product.
        category (str): The updated product category.
        subcategory (str): The updated product subcategory.
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
            print(f"Image upload error: {str(e)}")  # Log the error for debugging
            raise HTTPException(status_code=400, detail="Image upload failed: " + str(e))

    # Prepare the product update data using the Pydantic model
    product_data = schemas.ProductUpdate(
        name=name,
        producer=producer,
        description=description,
        price=price,
        stock=stock,
        category=category,
        subcategory=subcategory
    )

    # Pass the product data and image URL to the update function in crud.py
    updated_product = await crud.update_product(product_id=product_id, product=product_data, image_url=image_url)

    if updated_product is None:
        # If no product was updated, return a 404 error
        raise HTTPException(status_code=404, detail="Product not found")

    # Return the updated product data
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
