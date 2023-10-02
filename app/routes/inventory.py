from datetime import datetime, timedelta
from random import choice, randint
import faker
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Category, Inventory, InventoryHistory, Product, Sale
from sqlalchemy.orm import aliased
from sqlalchemy import func

router = APIRouter()

class InventoryUpdate(BaseModel):
    quantity: int

@router.get("/inventory")
def view_inventory():
    try:
        db = SessionLocal()
        # Retrieve all inventory items
        inventory = db.query(Inventory).all()

        # Convert inventory items to a list of dictionaries
        inventory_data = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "low_stock_threshold": item.low_stock_threshold,
                "last_updated": item.last_updated,
            }
            for item in inventory
        ]

        return {"inventory": inventory_data}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/inventory/low-stock-alerts")
def view_low_stock_alerts():
    try:
        db = SessionLocal()
        # Retrieve inventory items with low stock
        low_stock_items = db.query(Inventory).filter(Inventory.quantity <= Inventory.low_stock_threshold).all()

        # Convert low stock items to a list of dictionaries
        low_stock_data = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "low_stock_threshold": item.low_stock_threshold,
                "last_updated": item.last_updated,
            }
            for item in low_stock_items
        ]

        return {"low_stock_alerts": low_stock_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
class InventoryUpdate(BaseModel):
    quantity: int

@router.put("/inventory/{inventory_id}/update")
def update_inventory(inventory_id: int, inventory_update: InventoryUpdate):
    try:
        db = SessionLocal()
        inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory item not found")
        
        # Update the quantity and record the change in history with a new timestamp
        inventory.quantity = inventory_update.quantity
        db.add(inventory)
        
        # Insert a new record into inventory_history
        history_entry = InventoryHistory(inventory_id=inventory_id, quantity=inventory_update.quantity)
        db.add(history_entry)
        
        db.commit()
        db.refresh(inventory)
        
        return {"message": "Inventory updated successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()

@router.get("/inventory/{inventory_id}/history")
def get_inventory_history(inventory_id: int):
    try:
        db = SessionLocal()
        # Retrieve the historical changes for a specific inventory item
        inventory_history = (
            db.query(InventoryHistory)
            .filter(InventoryHistory.inventory_id == inventory_id)
            .order_by(InventoryHistory.timestamp)
            .all()
        )
        
        if not inventory_history:
            raise HTTPException(status_code=404, detail="Inventory history not found")

        return inventory_history
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()