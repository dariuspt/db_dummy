from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import os
from .routers import products, orders, categories, subcategories

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow only specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include the routers for your API endpoints
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(subcategories.router, prefix="/subcategories", tags=["Subcategories"])

# Serve static files like JS, CSS, fonts, etc., from the 'static/dist' folder
app.mount("/static", StaticFiles(directory="static/dist"), name="static")

# Serve index.html for the root URL
@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join('static', 'dist', 'index.html'))
