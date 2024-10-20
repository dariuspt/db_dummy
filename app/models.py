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
    category_id = Column(Integer, ForeignKey('topcategories.id'), nullable=True)
    subcategory = Column(String)
    image_url = Column(String, nullable=True)
    is_top_product = Column(Boolean, default=False)  # New boolean field for top products

    category = relationship("TopCategory", back_populates="products")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    product = relationship("Product")

class TopCategory(Base):
    __tablename__ = "topcategories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    is_top_category = Column(Boolean, default=False)  # New boolean field for top categories

    products = relationship("Product", back_populates="category")

class TopProduct(Base):
    __tablename__ = "topproducts"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    rank = Column(Integer)
    product = relationship("Product")
