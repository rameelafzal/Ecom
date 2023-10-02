from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace with your MySQL database URL
DATABASE_URL = "mysql+mysqlconnector://root:12345679@localhost:3306/ecom2"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
