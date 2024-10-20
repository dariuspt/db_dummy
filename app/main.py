from fastapi import FastAPI
from .routers import products, orders, topcategories, topproducts

app = FastAPI()

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(topcategories.router, prefix="/topcategories", tags=["Top Categories"])
app.include_router(topproducts.router, prefix="/topproducts", tags=["Top Products"])
