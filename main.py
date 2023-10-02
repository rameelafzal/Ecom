from fastapi import FastAPI
from app.routes import sales, products, revenue, inventory

app = FastAPI()

# Include the route modules
app.include_router(sales.router)
app.include_router(revenue.router)
app.include_router(inventory.router)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
