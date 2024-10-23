from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from . import models, schemas
from typing import Optional

# ================================
# CRUD for Products
# ================================

# Create a new product
async def create_product(db: AsyncSession, product: schemas.ProductCreate, image_url: Optional[str] = None):
    db_product = models.Product(
        name=product.name,
        producer=product.producer,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=product.category_id,
        subcategory_id=product.subcategory_id,
        is_top_product=product.is_top_product,
        image_url=image_url
    )

    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# Get all products with category and subcategory names
async def get_all_products(db: AsyncSession):
    result = await db.execute(
        select(models.Product)
        .options(
            joinedload(models.Product.category),
            joinedload(models.Product.subcategory)
        )
    )
    products = result.scalars().all()

    products_with_names = [
        {
            "id": product.id,
            "name": product.name,
            "producer": product.producer,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category_name": product.category.name if product.category else None,
            "subcategory_name": product.subcategory.name if product.subcategory else None,
            "image_url": product.image_url,
            "is_top_product": product.is_top_product,
        }
        for product in products
    ]

    return products_with_names

# Get a product by its ID with category and subcategory names
async def get_product_by_id(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(models.Product)
        .options(joinedload(models.Product.category), joinedload(models.Product.subcategory))
        .where(models.Product.id == product_id)
    )
    product = result.scalars().first()

    if product:
        product_data = {
            "id": product.id,
            "name": product.name,
            "producer": product.producer,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category_name": product.category.name if product.category else None,
            "subcategory_name": product.subcategory.name if product.subcategory else None,
            "image_url": product.image_url,
            "is_top_product": product.is_top_product,
        }
        return product_data
    return None

# Get a product by its name with category and subcategory names
async def get_product_by_name(db: AsyncSession, product_name: str):
    result = await db.execute(
        select(models.Product)
        .options(joinedload(models.Product.category), joinedload(models.Product.subcategory))
        .where(models.Product.name == product_name)
    )
    product = result.scalars().first()

    if product:
        product_data = {
            "id": product.id,
            "name": product.name,
            "producer": product.producer,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category_name": product.category.name if product.category else None,
            "subcategory_name": product.subcategory.name if product.subcategory else None,
            "image_url": product.image_url,
            "is_top_product": product.is_top_product,
        }
        return product_data
    return None

# Get a product with its associated category
async def get_product_with_category(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(models.Product)
        .options(
            joinedload(models.Product.category),
            joinedload(models.Product.subcategory)
        )
        .where(models.Product.id == product_id)
    )
    product = result.scalars().first()

    if product:
        product_data = {
            "id": product.id,
            "name": product.name,
            "producer": product.producer,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category_name": product.category.name if product.category else None,
            "subcategory_name": product.subcategory.name if product.subcategory else None,
            "image_url": product.image_url,
            "is_top_product": product.is_top_product,
        }
        return product_data
    return None

# Get all top products
async def get_top_products(db: AsyncSession):
    result = await db.execute(
        select(models.Product)
        .where(models.Product.is_top_product == True)
        .options(joinedload(models.Product.category), joinedload(models.Product.subcategory))  # Eager load relationships
    )
    top_products = result.scalars().all()

    top_products_with_names = [
        {
            "id": product.id,
            "name": product.name,
            "producer": product.producer,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category_name": product.category.name if product.category else None,
            "subcategory_name": product.subcategory.name if product.subcategory else None,
            "image_url": product.image_url,
            "is_top_product": product.is_top_product,
        }
        for product in top_products
    ]

    return top_products_with_names

# Update a product
async def update_product(db: AsyncSession, product: models.Product, updates: dict):
    """
    Updates an existing product with the provided fields.
    """
    # Update only the fields that are provided
    for key, value in updates.items():
        setattr(product, key, value)

    # Add the updated product object back to the session and commit the changes
    db.add(product)
    await db.commit()
    await db.refresh(product)

    return product

# Delete a product
async def delete_product(db: AsyncSession, db_product: models.Product):
    # Ensure the instance is an actual SQLAlchemy model
    if db_product:
        await db.delete(db_product)
        await db.commit()
        return db_product
    return None


async def get_product_by_id_only_delete(db: AsyncSession, product_id: int):
    # Helper function to fetch the product by ID
    result = await db.execute(select(models.Product).where(models.Product.id == product_id))
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
# CRUD for Categories
# ================================

# Create a new category
async def create_category(db: AsyncSession, category: schemas.CategoryCreate, image_url: Optional[str] = None):
    db_category = models.Category(
        name=category.name,
        description=category.description,
        is_top_category=category.is_top_category,
        image_url=image_url
    )

    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

# Get all categories
async def get_all_categories(db: AsyncSession):
    result = await db.execute(
        select(models.Category)
        .options(selectinload(models.Category.products), selectinload(models.Category.subcategories))
    )
    return result.scalars().all()


async def get_top_categories(db: AsyncSession):
    result = await db.execute(
        select(models.Category)
        .where(models.Category.is_top_category == True)
    )
    return result.scalars().all()  # Return a list of all top categories

# Get a category by its ID
async def get_category_by_id(db: AsyncSession, category_id: int):
    result = await db.execute(
        select(models.Category)
        .where(models.Category.id == category_id)
        .options(joinedload(models.Category.products))
    )
    return result.scalars().first()


async def get_category_by_name(db: AsyncSession, category_name: str):
    result = await db.execute(
        select(models.Category)
        .where(models.Category.name == category_name)
        .options(joinedload(models.Category.products))  # Eager load products
    )
    return result.scalars().first()

# Update a category by ID
async def update_category(db: AsyncSession, category: models.Category, updates: dict):
    # Update only the fields that are provided
    for key, value in updates.items():
        setattr(category, key, value)

    db.add(category)
    await db.commit()
    await db.refresh(category)

    # Return the updated category with subcategories
    return {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "is_top_category": category.is_top_category,
        "image_url": category.image_url,
        "subcategories": [
            {
                "id": sub.id,
                "name": sub.name,
                "category_name": category.name,
            } for sub in category.subcategories
        ]
    }



# Delete a category by ID
async def delete_category(db: AsyncSession, category_id: int):
    db_category = await get_category_by_id(db, category_id)
    if db_category:
        await db.delete(db_category)
        await db.commit()
    return db_category

# ================================
# Fetch Products by Category or Subcategory
# ================================
async def get_products_by_category(db: AsyncSession, category_id: int):
    result = await db.execute(
        select(models.Product)
        .where(models.Product.category_id == category_id)
        .options(joinedload(models.Product.category), joinedload(models.Product.subcategory))
    )
    products = result.scalars().all()

    products_with_names = [
        {
            "id": product.id,
            "name": product.name,
            "producer": product.producer,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category_name": product.category.name if product.category else None,
            "subcategory_name": product.subcategory.name if product.subcategory else None,
            "image_url": product.image_url,
            "is_top_product": product.is_top_product,
        }
        for product in products
    ]
    return products_with_names

async def get_products_by_subcategory(db: AsyncSession, subcategory_id: int):
    result = await db.execute(
        select(models.Product)
        .where(models.Product.subcategory_id == subcategory_id)
        .options(joinedload(models.Product.category), joinedload(models.Product.subcategory))
    )
    products = result.scalars().all()

    products_with_names = [
        {
            "id": product.id,
            "name": product.name,
            "producer": product.producer,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category_name": product.category.name if product.category else None,
            "subcategory_name": product.subcategory.name if product.subcategory else None,
            "image_url": product.image_url,
            "is_top_product": product.is_top_product,
        }
        for product in products
    ]
    return products_with_names

# ================================
# CRUD for Subcategories
# ================================

# Get all subcategories with associated category names
async def get_all_subcategories(db: AsyncSession):
    result = await db.execute(
        select(models.SubCategory)
        .options(joinedload(models.SubCategory.category))  # Load the associated category
    )
    subcategories = result.scalars().all()

    # Return subcategories with category names instead of IDs
    subcategories_with_names = [
        {
            "id": subcategory.id,
            "name": subcategory.name,
            "category_name": subcategory.category.name if subcategory.category else None
        }
        for subcategory in subcategories
    ]
    return subcategories_with_names

# Create a subcategory (still using category_id for creation)
async def create_subcategory(db: AsyncSession, subcategory: schemas.SubCategoryCreate):
    # Use the category_id directly since it's already resolved
    db_subcategory = models.SubCategory(name=subcategory.name, category_id=subcategory.category_identifier)
    db.add(db_subcategory)
    await db.commit()
    await db.refresh(db_subcategory)

    # Return the created subcategory with the associated category name
    result = await db.execute(
        select(models.SubCategory)
        .options(joinedload(models.SubCategory.category))
        .where(models.SubCategory.id == db_subcategory.id)
    )
    created_subcategory = result.scalars().first()

    if created_subcategory:
        return {
            "id": created_subcategory.id,
            "name": created_subcategory.name,
            "category_name": created_subcategory.category.name if created_subcategory.category else None
        }
    return None

# Get all subcategories for a specific category (by category_id)
async def get_subcategories(db: AsyncSession, category_id: int):
    result = await db.execute(
        select(models.SubCategory)
        .options(joinedload(models.SubCategory.category))
        .where(models.SubCategory.category_id == category_id)
    )
    subcategories = result.scalars().all()

    subcategories_with_names = [
        {
            "id": subcategory.id,
            "name": subcategory.name,
            "category_name": subcategory.category.name if subcategory.category else None
        }
        for subcategory in subcategories
    ]
    return subcategories_with_names

# Get a subcategory by its ID (including category name)
async def get_subcategory_by_id(db: AsyncSession, subcategory_id: int):
    result = await db.execute(
        select(models.SubCategory)
        .options(joinedload(models.SubCategory.category))  # Eager load the category relationship
        .where(models.SubCategory.id == subcategory_id)
    )
    subcategory = result.scalars().first()

    if subcategory:
        return {
            "id": subcategory.id,
            "name": subcategory.name,
            "category_name": subcategory.category.name if subcategory.category else None
        }
    return None


async def get_subcategory_by_id_for_update(db: AsyncSession, subcategory_id: int):
    result = await db.execute(
        select(models.SubCategory)
        .options(joinedload(models.SubCategory.category))  # Load the category relationship
        .where(models.SubCategory.id == subcategory_id)
    )
    return result.scalars().first()

# Get a subcategory by its name (including category name)
async def get_subcategory_by_name(db: AsyncSession, subcategory_name: str):
    result = await db.execute(
        select(models.SubCategory)
        .options(joinedload(models.SubCategory.category))  # Eager load the category relationship
        .where(models.SubCategory.name == subcategory_name)
    )
    subcategory = result.scalars().first()

    if subcategory:
        return {
            "id": subcategory.id,
            "name": subcategory.name,
            "category_name": subcategory.category.name if subcategory.category else None
        }
    return None

# Update a subcategory by its current object (with category name in the response)
async def update_subcategory(db: AsyncSession, subcategory: models.SubCategory, updates: dict):
    # Update only the fields that are provided
    for key, value in updates.items():
        setattr(subcategory, key, value)

    db.add(subcategory)
    await db.commit()
    await db.refresh(subcategory)

    # Return the updated subcategory with the associated category name
    return {
        "id": subcategory.id,
        "name": subcategory.name,
        "category_name": subcategory.category.name if subcategory.category else None
    }



# Delete a subcategory by its ID
async def delete_subcategory(db: AsyncSession, subcategory_id: int):
    # Retrieve the actual subcategory model instance to delete
    result = await db.execute(
        select(models.SubCategory)
        .where(models.SubCategory.id == subcategory_id)
    )
    db_subcategory = result.scalars().first()

    if db_subcategory:
        await db.delete(db_subcategory)  # Use the actual SQLAlchemy model instance
        await db.commit()
        return db_subcategory  # Return the deleted model instance if needed
    return None

