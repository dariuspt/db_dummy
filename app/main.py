from fastapi import FastAPI
from .routers import products, orders, categories, topproducts

app = FastAPI()

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(topproducts.router, prefix="/topproducts", tags=["Top Products"])
