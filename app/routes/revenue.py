from datetime import datetime, timedelta
from random import choice, randint
import faker
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Category, Product, Sale
from sqlalchemy.orm import aliased
from sqlalchemy import func

router = APIRouter()

@router.get("/revenue/daily")
def get_daily_revenue(
    date: str = Query(None, description="Date (YYYY-MM-DD)"),
):
    try:
        db = SessionLocal()
        if date is None:
            # If date is not provided, default to today's date
            date = datetime.now().strftime("%Y-%m-%d")

        # Calculate daily revenue
        daily_revenue = (
            db.query(func.date(Sale.sale_date).label("day"), func.sum(Product.price * Sale.quantity).label("revenue"))
            .join(Product)
            .filter(func.date(Sale.sale_date) == date)
            .group_by(func.date(Sale.sale_date))
            .first()
        )

        if not daily_revenue:
            return {"date": date, "daily_revenue": 0.0}

        return {"date": daily_revenue.day.strftime("%Y-%m-%d"), "daily_revenue": float(daily_revenue.revenue)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/revenue/weekly")
def get_weekly_revenue(
):
    try:
        # Calculate the start and end dates for the current week
        db = SessionLocal()
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Calculate weekly revenue
        weekly_revenue = (
            db.query(func.date(Sale.sale_date).label("start_date"), func.sum(Product.price * Sale.quantity).label("revenue"))
            .join(Product)
            .filter(func.date(Sale.sale_date) >= start_of_week, func.date(Sale.sale_date) <= end_of_week)
            .group_by(func.date(Sale.sale_date))
            .first()
        )

        if not weekly_revenue:
            return {"start_date": start_of_week.strftime("%Y-%m-%d"), "end_date": end_of_week.strftime("%Y-%m-%d"), "weekly_revenue": 0.0}

        return {"start_date": weekly_revenue.start_date.strftime("%Y-%m-%d"), "end_date": end_of_week.strftime("%Y-%m-%d"), "weekly_revenue": float(weekly_revenue.revenue)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/revenue/monthly")
def get_monthly_revenue(
):
    try:
        # Calculate the start and end dates for the current month
        db = SessionLocal()
        today = datetime.now()
        start_of_month = today.replace(day=1)
        end_of_month = (today.replace(day=1, month=today.month + 1) - timedelta(days=1))

        # Calculate monthly revenue
        monthly_revenue = (
            db.query(func.date(Sale.sale_date).label("start_date"), func.sum(Product.price * Sale.quantity).label("revenue"))
            .join(Product)
            .filter(func.date(Sale.sale_date) >= start_of_month, func.date(Sale.sale_date) <= end_of_month)
            .group_by(func.date(Sale.sale_date))
            .first()
        )

        if not monthly_revenue:
            return {"start_date": start_of_month.strftime("%Y-%m-%d"), "end_date": end_of_month.strftime("%Y-%m-%d"), "monthly_revenue": 0.0}

        return {"start_date": monthly_revenue.start_date.strftime("%Y-%m-%d"), "end_date": end_of_month.strftime("%Y-%m-%d"), "monthly_revenue": float(monthly_revenue.revenue)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/revenue/annual")
def get_annual_revenue(
):
    try:
        # Calculate the start and end dates for the current year
        db = SessionLocal()
        today = datetime.now()
        start_of_year = today.replace(day=1, month=1)
        end_of_year = today.replace(day=31, month=12)

        # Calculate annual revenue
        annual_revenue = (
            db.query(func.date(Sale.sale_date).label("start_date"), func.sum(Product.price * Sale.quantity).label("revenue"))
            .join(Product)
            .filter(func.date(Sale.sale_date) >= start_of_year, func.date(Sale.sale_date) <= end_of_year)
            .group_by(func.date(Sale.sale_date))
            .first()
        )

        if not annual_revenue:
            return {"start_date": start_of_year.strftime("%Y-%m-%d"), "end_date": end_of_year.strftime("%Y-%m-%d"), "annual_revenue": 0.0}

        return {"start_date": annual_revenue.start_date.strftime("%Y-%m-%d"), "end_date": end_of_year.strftime("%Y-%m-%d"), "annual_revenue": float(annual_revenue.revenue)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.get("/revenue")
def get_revenue(
    category_id: int = Query(..., description="Category ID"),
    start_date: str = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date (YYYY-MM-DD)"),
):
    try:
        db = SessionLocal()
        # Check if the category exists
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        # Calculate revenue
        revenue = (
            db.query(func.sum(Sale.quantity * Product.price))
            .join(Sale.product)
            .filter(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date,
                Sale.product.has(category_id=category_id)
            )
            .scalar()
        )
        
        return {"category_id": category_id, "start_date": start_date, "end_date": end_date, "revenue": revenue}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()