from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Table, CheckConstraint, DateTime, func
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
    order_products = relationship('OrderProduct', back_populates='product')


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    processed = Column(Boolean, default=False)  # New boolean field

    order_products = relationship('OrderProduct', back_populates='order', lazy='selectin')


class OrderProduct(Base):
    __tablename__ = 'order_products'
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    order = relationship('Order', back_populates='order_products')
    product = relationship('Product', back_populates='order_products')


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