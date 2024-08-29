from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Base schema for product properties
class ProductBase(BaseModel):
    name: str  # Name of the product (required)
    description: Optional[str] = None  # Description of the product (optional)
    price: float  # Price of the product (required)
    stock: int  # Stock of the product (required)

# Schema for creating a product
class ProductCreate(ProductBase):
    pass  # Inherits fields from ProductBase

# Schema for updating a product
class ProductUpdate(ProductBase):
    pass  # Inherits fields from ProductBase

# Schema for a product response that includes an ID
class Product(ProductBase):
    id: int  # Unique identifier for the product

    class Config:
        orm_mode = True  # Enables compatibility with ORM models

# Schema for creating an order item
class OrderItemCreate(BaseModel):
    product_id: int  # ID of the product being ordered
    quantity: int  # Quantity of the product being ordered

# Schema for updating an order item (e.g., changing quantity)
class OrderItemUpdate(BaseModel):
    quantity: int  # New quantity of the product being ordered

# Schema for an order item response that includes product details
class OrderItem(BaseModel):
    product_id: int  # ID of the product
    quantity: int  # Quantity of the product
    product_name: str  # Name of the product (from OrderItem)
    product_price: float  # Price of the product

    class Config:
        orm_mode = True  # Enables compatibility with ORM models

# Schema for creating an order with multiple items
class OrderCreate(BaseModel):
    order_items: List[OrderItemCreate]  # List of items in the order

# Schema for an order response that includes an ID and its items
class Order(BaseModel):
    id: int  # Unique identifier for the order
    created_at: datetime  # Timestamp for when the order was created
    order_items: List[OrderItem]  # List of items in the order

    class Config:
        orm_mode = True  # Enables compatibility with ORM models
