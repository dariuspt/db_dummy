from fastapi import APIRouter, HTTPException
from .. import crud, schemas

# Create an APIRouter instance for product-related routes
router = APIRouter()


# Create a new product
@router.post("/", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate):
    """
    Create a new product in the database.

    Args:
        product (schemas.ProductCreate): The product data to create.

    Returns:
        schemas.Product: The created product data, including its ID.
    """
    return await crud.create_product(product)


# Get a product by ID
@router.get("/{product_id}", response_model=schemas.Product)
async def read_product(product_id: int):
    """
    Retrieve a product by its ID.

    Args:
        product_id (int): The ID of the product to retrieve.

    Returns:
        schemas.Product: The product data if found.

    Raises:
        HTTPException: If the product is not found.
    """
    product = await crud.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Get all products
@router.get("/", response_model=list[schemas.Product])  # Ensure response is a list of products
async def get_products():
    """
    Retrieve all products from the database.

    Returns:
        list[schemas.Product]: A list of all products.
    """
    return await crud.get_all_products()


# Update a product by ID
@router.put("/{product_id}", response_model=schemas.Product)
async def update_product(product_id: int, product: schemas.ProductUpdate):
    """
    Update an existing product by its ID.

    Args:
        product_id (int): The ID of the product to update.
        product (schemas.ProductUpdate): The updated product data.

    Returns:
        schemas.Product: The updated product data if successful.

    Raises:
        HTTPException: If the product is not found.
    """
    updated_product = await crud.update_product(product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


# Delete a product by ID
@router.delete("/{product_id}")
async def delete_product(product_id: int):
    """
    Delete a product by its ID.

    Args:
        product_id (int): The ID of the product to delete.

    Returns:
        dict: A success message indicating the product was deleted.

    Raises:
        HTTPException: If the product is not found.
    """
    success = await crud.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}
