from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 
from sqlalchemy.sql import func
Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String) 
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")
    sales = relationship("Sale", back_populates="product")
    inventory = relationship("Inventory", back_populates="product")


class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    sale_date = Column(DateTime)
    quantity = Column(Integer)
    product = relationship("Product", back_populates="sales")

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    low_stock_threshold = Column(Integer)
    last_updated = Column(DateTime)
    product = relationship("Product", back_populates="inventory")
    history = relationship("InventoryHistory", back_populates="inventory")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class InventoryHistory(Base):
    __tablename__ = "inventory_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"))
    quantity = Column(Integer)
    timestamp = Column(TIMESTAMP, server_default=func.now())

    # Define the foreign key relationship
    inventory = relationship("Inventory", back_populates="history")