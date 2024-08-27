from fastapi import FastAPI  # Import FastAPI framework
from .database import database, engine, metadata  # Import database connection, engine, and metadata
from .routers import products  # Import the products router for handling product-related routes
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware for handling CORS

# Create the database tables if they don't exist already
metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI()

# Include the products router with a prefix and tags for easier API documentation
app.include_router(products.router, prefix="/products", tags=["products"])

# Add middleware to handle CORS (Cross-Origin Resource Sharing) issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL if needed for security
    allow_credentials=True,  # Allow credentials to be included in requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers in requests
)

# Event to run when the application starts up
@app.on_event("startup")
async def startup():
    await database.connect()  # Connect to the database

# Event to run when the application shuts down
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()  # Disconnect from the database
