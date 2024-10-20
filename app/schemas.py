from pydantic import BaseModel
from typing import List, Optional

# Product schemas
class ProductCreate(BaseModel):
    name: str
    producer: Optional[str] = None
    description: Optional[str] = None
    price: float
    stock: int
    category_id: Optional[int] = None  # Use category_id if referring to the ID
    subcategory: Optional[str] = None
    image_url: Optional[str] = None
    is_top_product: Optional[bool] = None  # Add this field for top products

    class Config:
        orm_mode = True
class Product(ProductCreate):
    id: int

    class Config:
        orm_mode = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    producer: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None
    subcategory: Optional[str] = None
    image_url: Optional[str] = None
    is_top_product: Optional[bool] = None  # Add this field for top products

    class Config:
        orm_mode = True

# Order schemas
class OrderBase(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True

class OrderUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    order_date: Optional[str] = None  # You can use a date type if needed

    class Config:
        orm_mode = True

# TopCategory schemas
class TopCategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_top_category: Optional[bool] = None  # Add this field for top categories

# Schema for returning a top category
class TopCategory(TopCategoryCreate):
    id: int
    image_url: Optional[str] = None

    class Config:
        orm_mode = True

class TopCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_top_category: Optional[bool] = None  # Add this field for top categories

    class Config:
        orm_mode = True

# TopProduct schemas
class TopProductBase(BaseModel):
    product_id: int
    rank: int

class TopProductCreate(TopProductBase):
    pass

class TopProduct(TopProductBase):
    id: int

    class Config:
        orm_mode = True

class TopProductUpdate(BaseModel):
    product_id: Optional[int] = None
    rank: Optional[int] = None
    highlighted: Optional[bool] = None

    class Config:
        orm_mode = True