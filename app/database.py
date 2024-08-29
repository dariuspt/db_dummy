from sqlalchemy import create_engine, MetaData  # Import necessary functions from SQLAlchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession  # Import async engine and session
from sqlalchemy.orm import sessionmaker  # Import sessionmaker for creating database sessions
from sqlalchemy.ext.declarative import declarative_base  # Import Base for ORM model declaration
from databases import Database  # Import the Database class for async database operations
from .config import DATABASE_URL  # Import the database URL from the config module

# Create an instance of the Database class for asynchronous operations
database = Database(DATABASE_URL)

# Create a MetaData instance to hold information about the database schema
metadata = MetaData()

# Create an asynchronous SQLAlchemy engine instance for async database operations
async_engine = create_async_engine(DATABASE_URL, echo=True)  # This engine is used for async sessions

# Create a configured "Session" class for asynchronous sessions
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Avoids automatic expiration of objects after commit
    autoflush=False,
    autocommit=False
)

# Dependency to get the async database session
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session  # Yield the session to be used by FastAPI routes

# Synchronous engine for running migrations (if needed)
sync_engine = create_engine(DATABASE_URL)  # This engine is used for creating sessions or running migrations

# Create a configured "Session" class for synchronous sessions (used in migrations)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Dependency to get the synchronous database session (if needed)
def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Yield the session to be used by FastAPI routes
    finally:
        db.close()  # Ensure the session is closed after use

Base = declarative_base(metadata=metadata)  # Create a base class for declarative models
