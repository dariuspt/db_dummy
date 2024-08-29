from fastapi import APIRouter, HTTPException, Depends  # Import necessary FastAPI classes
from sqlalchemy.orm import Session  # Import Session for database operations
from .. import crud, schemas  # Import CRUD operations and Pydantic schemas
from ..database import get_db  # Import the database session dependency

router = APIRouter()  # Create a new router instance

# Create a new product
@router.post("/", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.

    Args:
        product (ProductCreate): The product data to create.
        db (Session): The database session dependency.

    Returns:
        Product: The created product data.
    """
    return await crud.create_product(product)  # Call the CRUD function to create the product

# Get a product by ID
@router.get("/{product_id}", response_model=schemas.Product)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a product by its ID.

    Args:
        product_id (int): The ID of the product to retrieve.
        db (Session): The database session dependency.

    Returns:
        Product: The product data.
    """
    product = await crud.get_product(product_id)  # Call the CRUD function to get the product
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")  # Raise 404 if product not found
    return product  # Return the found product

# Get all products
@router.get("/", response_model=list[schemas.Product])
async def get_products(db: Session = Depends(get_db)):
    """
    Retrieve all products.

    Args:
        db (Session): The database session dependency.

    Returns:
        List[Product]: A list of products.
    """
    return await crud.get_all_products()  # Call the CRUD function to get all products

# Update a product by ID
@router.put("/{product_id}", response_model=schemas.Product)
async def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    """
    Update an existing product by its ID.

    Args:
        product_id (int): The ID of the product to update.
        product (ProductUpdate): The updated product data.
        db (Session): The database session dependency.

    Returns:
        Product: The updated product data.
    """
    updated_product = await crud.update_product(product_id, product)  # Call the CRUD function to update the product
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")  # Raise 404 if product not found
    return updated_product  # Return the updated product

# Delete a product by ID
@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product by its ID.

    Args:
        product_id (int): The ID of the product to delete.
        db (Session): The database session dependency.

    Returns:
        dict: Confirmation message.
    """
    success = await crud.delete_product(product_id)  # Call the CRUD function to delete the product
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")  # Raise 404 if product not found
    return {"detail": "Product deleted"}  # Return confirmation message
