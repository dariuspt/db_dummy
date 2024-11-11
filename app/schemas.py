from pydantic import BaseModel
from typing import List, Optional, Union

# Product schemas
class ProductCreate(BaseModel):
    name: str
    producer: Optional[str] = None
    description: Optional[str] = None
    price: float
    stock: int
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    image_url: Optional[str] = None
    is_top_product: Optional[bool] = None

    class Config:
        orm_mode = True

class Product(BaseModel):
    id: int
    name: str
    producer: Optional[str] = None
    description: Optional[str] = None
    price: float
    stock: int
    category_name: Optional[str] = None  # Use category name instead of ID
    subcategory_name: Optional[str] = None  # Use subcategory name instead of ID
    image_url: Optional[str] = None
    is_top_product: Optional[bool] = None

    class Config:
        orm_mode = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    producer: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_name: Optional[str] = None  # Use category name instead of ID
    subcategory_name: Optional[str] = None  # Use subcategory name instead of ID
    image_url: Optional[str] = None
    is_top_product: Optional[bool] = None

    class Config:
        from_attributes = True  # Updated to from_attributes


# Order detail schema to represent each product in an order
class ProductInOrder(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    products: List[ProductInOrder]

    class Config:
        orm_mode = True

class Order(BaseModel):
    id: int
    products: List[ProductInOrder]

    class Config:
        orm_mode = True

# SubCategory schemas
class SubCategoryCreate(BaseModel):
    name: Optional[str] = None
    category_identifier: Optional[Union[int, str]] = None

class SubCategoryUpdate(BaseModel):
    name: Optional[str] = None
    category_identifier: Optional[Union[int, str]] = None  # Can accept either category ID or name

    class Config:
        from_attributes = True

class SubCategory(BaseModel):
    id: int
    name: Optional[str] = None
    category_name: Optional[str] = None  # Include the category name in the response

    class Config:
        from_attributes = True  # Updated to from_attributes


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
