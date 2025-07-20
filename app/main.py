from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import connect_to_mongo, close_mongo_connection

# Import routes
import app.api.products as products
import app.api.orders as orders

app = FastAPI(title="E-commerce API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route
@app.get("/")
async def root():
    return {
        "message": "Welcome to E-commerce API",
        "endpoints": {
            "products": "/products",
            "orders": "/orders"
        },
        "documentation": "/docs"
    }

# Include routers
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])

# Database connection events
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()
    
@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 