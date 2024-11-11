from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL

# Configure the async engine with connection pool settings
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,             # Set the number of connections in the pool
    max_overflow=10,          # Allow a few overflow connections if the pool is exhausted
    pool_timeout=30,          # Set timeout (in seconds) for acquiring a connection from the pool
    pool_recycle=1800,        # Recycle (close) connections after 30 minutes (1800 seconds)
    pool_pre_ping=True        # Check connections before using them to ensure they are valid
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Define the base class for models
Base = declarative_base()

# Dependency to get the database session
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


