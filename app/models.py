from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    producer = Column(String)
    description = Column(String, nullable=True)
    price = Column(Float)
    stock = Column(Integer)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"), nullable=True)
    image_url = Column(String, nullable=True)
    is_top_product = Column(Boolean)  # New boolean field for top products

    category = relationship("Category", back_populates="products")
    subcategory = relationship("SubCategory", back_populates="products")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    product = relationship("Product")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    is_top_category = Column(Boolean, default=False)  # New boolean field for top categories

    subcategories = relationship("SubCategory", back_populates="category", lazy="selectin") # Relationship with subcategories
    products = relationship("Product", back_populates="category")


class SubCategory(Base):
    __tablename__ = "subcategories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))  # Foreign key to Category

    category = relationship("Category", back_populates="subcategories")  # Back-reference to Category
    products = relationship("Product", back_populates="subcategory")  # Relationship with products