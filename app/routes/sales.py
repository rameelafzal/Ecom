from datetime import datetime, timedelta
from random import choice, randint
import faker
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Category, Product, Sale
from sqlalchemy.orm import aliased

router = APIRouter()


class SaleCreate(BaseModel):
    product_id: int
    quantity: int

@router.get("/sales/{sale_id}")
def get_sales(sale_id: int):
    # Retrieve a sale record by its ID\
    db = SessionLocal()
    try:
        sale = db.query(Sale).filter(Sale.id == sale_id).first()
        if not sale:
            raise HTTPException(status_code=404, detail="Sale not found")
        return sale
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/sales/")
def get_sales_by_date_range(
    page: int = Query(1, description="Page number", ge=1),
    items_per_page: int = Query(10, description="Number of items per page", le=100),
    start_date: str = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date (YYYY-MM-DD)"),
):
    db = SessionLocal()
    try:
        # Calculate the offset based on the requested page and items per page
        offset = (page - 1) * items_per_page

        # Calculate the start and end dates for the query
        if start_date is None:
            # If start_date is not provided, set it to one year ago from today
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        if end_date is None:
            # If end_date is not provided, set it to today
            end_date = datetime.now().strftime("%Y-%m-%d")

        # Parse the dates into datetime objects
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

        # Query sales records within the specified date range with pagination
        sales = (
            db.query(Sale)
            .filter(Sale.sale_date >= start_datetime, Sale.sale_date <= end_datetime)
            .offset(offset)
            .limit(items_per_page)
            .all()
        )

        if not sales:
            raise HTTPException(status_code=404, detail="No sales records found")

        return sales
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()

@router.get("/categories/{category_id}/sales")
def get_sales_by_category(category_id: int):
    try:
        # Create a session
        db = SessionLocal()

        # Check if the category exists
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        # Retrieve sales by category
        sales = (
            db.query(Sale)
            .join(Product)  # Join with Product table
            .filter(Product.category_id == category_id)
            .all()
        )

        if not sales:
            raise HTTPException(status_code=404, detail="No sales records found for the category")
        return sales
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()

@router.get("/products/{product_id}/sales")
def get_sales_by_product(product_id: int):
    try:
        # Create a session
        db = SessionLocal()

        # Check if the product exists
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Retrieve sales by product
        sales = (
            db.query(Sale)
            .filter(Sale.product_id == product_id)
            .all()
        )

        if not sales:
            raise HTTPException(status_code=404, detail="No sales records found for the product")
        return sales
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()