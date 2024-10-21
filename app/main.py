from fastapi import FastAPI
from .routers import products, orders, categories, topproducts
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow only specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(topproducts.router, prefix="/topproducts", tags=["Top Products"])
