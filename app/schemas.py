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
    subcategory_id: Optional[int] = None  # Fixed to be an int
    image_url: Optional[str] = None
    is_top_product: Optional[bool] = None  # Add this field for top products

    class Config:
        from_attributes = True  # Use the updated from_attributes for Pydantic v2

class Product(ProductCreate):
    id: int

    class Config:
        from_attributes = True  # Updated to from_attributes

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    producer: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None  # Fixed to be an int
    image_url: Optional[str] = None
    is_top_product: Optional[bool] = None

    class Config:
        from_attributes = True  # Updated to from_attributes


# Order schemas
class OrderBase(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True  # Updated to from_attributes

class OrderUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    order_date: Optional[str] = None  # You can use a date type if needed

    class Config:
        from_attributes = True


# SubCategory schemas
class SubCategoryCreate(BaseModel):
    name: str
    category_id: int  # Foreign key to Category

class SubCategory(BaseModel):
    id: int
    name: str
    category_id: int

    class Config:
        from_attributes = True  # Updated to from_attributes


# Category schemas
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_top_category: Optional[bool] = None  # Add this field for top categories

class Category(CategoryCreate):
    id: int
    image_url: Optional[str] = None
    subcategories: List[SubCategory] = []

    class Config:
        from_attributes = True  # Updated to from_attributes

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_top_category: Optional[bool] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True
