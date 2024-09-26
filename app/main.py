from fastapi import FastAPI, Depends  # Import FastAPI and Depends for dependency injection
from .database import database, metadata, get_db  # Import database connection and get_db dependency
from .routers import products, orders, order_items  # Import the routers
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from sqlalchemy.orm import Session  # To manage database sessions
from sqlalchemy import create_engine

# Initialize the FastAPI application
app = FastAPI()

# Include the routers for products, orders, and order_items
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(order_items.router, prefix="/order_items", tags=["order_items"])

# Add middleware to handle CORS (Cross-Origin Resource Sharing) issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for testing purposes)
    allow_credentials=True,  # Allow cookies to be sent with cross-origin requests
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Dependency for providing database sessions
def get_db():
    db = database.sessionmaker()  # Create a new session
    try:
        yield db  # Provide the session to the request
    finally:
        db.close()  # Ensure the session is closed after the request


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
