from fastapi import FastAPI, Depends  # Import FastAPI and Depends for dependency injection
from .database import database, metadata  # Import database connection and metadata
from .routers import products, orders, order_items  # Import the routers
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL  # Import the database URL and Cloudinary config from config.py
import cloudinary
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Initialize the FastAPI application
app = FastAPI()

# Add middleware to handle CORS (Cross-Origin Resource Sharing) issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for testing purposes)
    allow_credentials=True,  # Allow cookies to be sent with cross-origin requests
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Create a new database engine using the asyncpg driver
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session maker bound to the engine
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency for providing database sessions
async def get_db():
    async with async_session_maker() as session:
        yield session  # Provide the session to the request


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Event to run when the application starts up
@app.on_event("startup")
async def startup():
    await database.connect()  # Connect to the database when the application starts


# Event to run when the application shuts down
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()  # Disconnect from the database when the application stops


# Include the routers for products, orders, and order_items
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(order_items.router, prefix="/order_items", tags=["order_items"])
