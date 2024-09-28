from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    """
    The Product model represents the products that are sold in the store.
    It contains fields for basic product information like name, producer, price, stock, and image URL.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    name = Column(String, index=True, nullable=False)  # Name of the product, must be unique and cannot be null
    producer = Column(String, index=True, nullable=False)  # Producer of the product, cannot be null
    description = Column(Text, nullable=True)  # Optional description of the product (Text allows long descriptions)
    price = Column(Float, nullable=False)  # Price of the product, must be greater than 0
    stock = Column(Integer, nullable=False)  # Stock quantity of the product, must be non-negative
    category = Column(String, nullable=True)  # Product category (optional)
    subcategory = Column(String, nullable=True)  # Product subcategory (optional)
    image_url = Column(String, nullable=True)  # URL to store product image (optional)

    # Relationship to OrderItem; one Product can be associated with multiple OrderItems
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    """
    The Order model represents a customer order in the system.
    It contains a timestamp for when the order was created.
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)  # Primary key for the order
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  # Timestamp for when the order was created

    # Relationship to OrderItem; one Order can have multiple OrderItems
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    """
    The OrderItem model represents an item within an order.
    It links the order to the product and includes the quantity of the product ordered.
    """
    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True)  # Foreign key referencing orders
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)  # Foreign key referencing products
    quantity = Column(Integer, nullable=False)  # Quantity of the product ordered

    # Fields to store product details
    product_name = Column(String, nullable=False)  # Name of the product being ordered
    product_price = Column(Float, nullable=False)  # Price of the product being ordered

    # Relationships to Product and Order; defining the bidirectional relationship
    product = relationship("Product", back_populates="order_items")
    order = relationship("Order", back_populates="order_items")
