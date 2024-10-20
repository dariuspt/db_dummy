from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from . import models, schemas
from typing import Optional

# ================================
# CRUD for Products
# ================================

# Create a new product
async def create_product(db: AsyncSession, product: schemas.ProductCreate, image_url: Optional[str] = None):
    # Create a new product instance
    db_product = models.Product(
        name=product.name,
        producer=product.producer,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=product.category_id,  # Use the resolved category_id
        subcategory=product.subcategory,
        is_top_product=product.is_top_product,
        image_url=image_url  # Use the image_url passed from the route
    )

    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)  # Refresh the instance to return the newly created product
    return db_product

# Get all products with optional pagination
async def get_all_products(db: AsyncSession):
    result = await db.execute(select(models.Product))
    return result.scalars().all()

# Get a product by its ID
async def get_product_by_id(db: AsyncSession, product_id: int):
    result = await db.execute(select(models.Product).where(models.Product.id == product_id))
    return result.scalars().first()

# Update a product
async def update_product(db: AsyncSession, product: models.Product, updates: schemas.ProductUpdate):
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

# Delete a product
async def delete_product(db: AsyncSession, product_id: int):
    db_product = await get_product_by_id(db, product_id)
    if db_product:
        await db.delete(db_product)
        await db.commit()
    return db_product


# Get a product with its associated category
async def get_product_with_category(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(models.Product).where(models.Product.id == product_id).options(joinedload(models.Product.category))
    )
    return result.scalars().first()

# ================================
# CRUD for Orders
# ================================

# Create a new order
async def create_order(db: AsyncSession, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

# Get all orders with optional pagination
async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Order).offset(skip).limit(limit).options(joinedload(models.Order.product))
    )
    return result.unique().scalars().all()

# Get an order by its ID
async def get_order_by_id(db: AsyncSession, order_id: int):
    result = await db.execute(select(models.Order).where(models.Order.id == order_id))
    return result.scalars().first()

# Update an order
async def update_order(db: AsyncSession, order: models.Order, updates: schemas.OrderUpdate):
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(order, key, value)

    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order

# Delete an order
async def delete_order(db: AsyncSession, order_id: int):
    db_order = await get_order_by_id(db, order_id)
    if db_order:
        await db.delete(db_order)
        await db.commit()
    return db_order

# ================================
# CRUD for Top Categories
# ================================

# Create a new category (no restrictions on top category)
async def create_category(db: AsyncSession, category: schemas.TopCategoryCreate, image_url: Optional[str] = None):
    # Create a new TopCategory instance
    db_category = models.TopCategory(
        name=category.name,
        description=category.description,
        image_url=image_url  # Use the image_url passed from the route
    )

    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)  # Refresh the instance to return the newly created category
    return db_category

# Get all categories (no filtering for top categories)
async def get_all_categories(db: AsyncSession):
    result = await db.execute(
        select(models.TopCategory)
        .options(joinedload(models.TopCategory.products))  # Eager load products
    )
    return result.unique().scalars().all()

# Get only top categories (is_top_category=True)
async def get_top_categories(db: AsyncSession):
    result = await db.execute(
        select(models.TopCategory)
        .where(models.TopCategory.is_top_category == True)
        .options(joinedload(models.TopCategory.products))  # Eager load products
    )
    return result.unique().scalars().all()

# Get a category by its ID
async def get_category_by_id(db: AsyncSession, category_id: int):
    result = await db.execute(
        select(models.TopCategory)
        .where(models.TopCategory.id == category_id)
        .options(joinedload(models.TopCategory.products))  # Eager load products
    )
    return result.scalars().first()

# Update a category by ID
async def update_category(db: AsyncSession, category: models.TopCategory, updates: schemas.TopCategoryUpdate):
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)

    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category

# Delete a category by ID
async def delete_category(db: AsyncSession, category_id: int):
    db_category = await get_category_by_id(db, category_id)
    if db_category:
        await db.delete(db_category)
        await db.commit()
    return db_category

# Get a category by ID with its associated products
async def get_category_with_products(db: AsyncSession, category_id: int):
    result = await db.execute(
        select(models.TopCategory)
        .where(models.TopCategory.id == category_id)
        .options(joinedload(models.TopCategory.products))  # Eager load products
    )
    return result.scalars().first()


# ================================
# CRUD for Top Products
# ================================

# Create a new top product
async def create_top_product(db: AsyncSession, top_product: schemas.TopProductCreate):
    db_top_product = models.TopProduct(**top_product.dict())
    db.add(db_top_product)
    await db.commit()
    await db.refresh(db_top_product)
    return db_top_product

# Get all top products with optional pagination
async def get_top_products(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.TopProduct).offset(skip).limit(limit).options(joinedload(models.TopProduct.product))
    )
    return result.unique().scalars().all()

# Get a top product by its ID
async def get_top_product_by_id(db: AsyncSession, top_product_id: int):
    result = await db.execute(select(models.TopProduct).where(models.TopProduct.id == top_product_id))
    return result.scalars().first()

# Update a top product
async def update_top_product(db: AsyncSession, top_product: models.TopProduct, updates: schemas.TopProductUpdate):
    # Apply updates dynamically
    update_data = updates.dict(exclude_unset=True)  # Only update fields that are provided
    for key, value in update_data.items():
        setattr(top_product, key, value)  # Update each field

    db.add(top_product)
    await db.commit()
    await db.refresh(top_product)  # Refresh the instance to get the updated data
    return top_product

# Delete a top product
async def delete_top_product(db: AsyncSession, top_product_id: int):
    db_top_product = await get_top_product_by_id(db, top_product_id)
    if db_top_product:
        await db.delete(db_top_product)
        await db.commit()
    return db_top_product

async def get_top_products(db: AsyncSession):
    result = await db.execute(select(models.Product).where(models.Product.is_top_product == True))
    return result.scalars().all()
