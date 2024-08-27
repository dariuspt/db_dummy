from pydantic import BaseModel

# Base model for product properties, shared across all product schemas
class ProductBase(BaseModel):
    name: str  # Name of the product (required)
    description: str  # Description of the product (optional)
    price: float  # Price of the product (required)


# Schema for creating a product
class ProductCreate(ProductBase):
    """Schema for creating a new product."""
    pass  # Inherits all fields from ProductBase


# Schema for updating a product
class ProductUpdate(ProductBase):
    """Schema for updating an existing product."""
    pass  # Inherits all fields from ProductBase


# Schema for a product with an ID, used in responses
class Product(ProductBase):
    """Schema for a product with an assigned ID."""
    id: int  # Unique identifier for the product

    class Config:
        orm_mode = True  # Enable ORM mode to allow compatibility with database models
