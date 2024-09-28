from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# --- Product Schemas ---

class ProductBase(BaseModel):
    """
    Base schema for product properties.
    """
    name: str  # Name of the product (required)
    producer: str  # Producer of the product (required)
    description: Optional[str] = None  # Description of the product (optional)
    price: float  # Price of the product (required)
    stock: int  # Stock of the product (required)
    category: str  # Category of the product (required)
    subcategory: str  # Subcategory of the product (required)

# Schema for creating a product
class ProductCreate(ProductBase):
    """
    Schema for creating a product.
    """
    pass  # Inherits fields from ProductBase

# Schema for updating a product
class ProductUpdate(ProductBase):
    """
    Schema for updating a product.
    """
    pass  # Inherits fields from ProductBase

# Schema for a product response that includes an ID and image_url
class Product(ProductBase):
    """
    Schema for returning product data, including ID and optional image_url.
    """
    id: int  # Unique identifier for the product
    image_url: Optional[str]  # URL of the product image (optional)

    class Config:
        orm_mode = True  # Enables compatibility with ORM models


# --- Order Item Schemas ---

class OrderItemCreate(BaseModel):
    """
    Schema for creating an order item.
    """
    product_id: int  # ID of the product being ordered
    quantity: int  # Quantity of the product being ordered

# Schema for updating an order item (e.g., changing quantity)
class OrderItemUpdate(BaseModel):
    """
    Schema for updating the quantity of an order item.
    """
    quantity: int  # New quantity of the product being ordered

# Schema for returning an order item response that includes product details
class OrderItem(BaseModel):
    """
    Schema for returning order item data, including product details.
    """
    product_id: int  # ID of the product
    quantity: int  # Quantity of the product
    product_name: str  # Name of the product (from OrderItem)
    product_price: float  # Price of the product

    class Config:
        orm_mode = True  # Enables compatibility with ORM models


# --- Order Schemas ---

class OrderCreate(BaseModel):
    """
    Schema for creating an order with multiple items.
    """
    order_items: List[OrderItemCreate]  # List of items in the order

class Order(BaseModel):
    """
    Schema for returning an order response that includes an ID and its items.
    """
    id: int  # Unique identifier for the order
    created_at: datetime  # Timestamp for when the order was created
    order_items: List[OrderItem]  # List of items in the order

    class Config:
        orm_mode = True  # Enables compatibility with ORM models
