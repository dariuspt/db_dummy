from fastapi import FastAPI  # Import FastAPI to create the application
from .database import database, metadata  # Import database connection and metadata for models
from .routers import products, orders, order_items  # Import the products router for managing product-related endpoints
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware

# Create the database tables if they don't exist already

# Initialize the FastAPI application
app = FastAPI()

# Include the products router with a prefix and tags for easier API documentation
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
