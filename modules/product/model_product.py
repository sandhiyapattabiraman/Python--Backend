from sqlmodel import SQLModel, Field, select
from ..utils.database import Session, engine
from uuid import uuid4, UUID
from datetime import datetime, timezone
from enum import Enum

def generate_timestamp():
    return datetime.now(timezone.utc)

class Categories(str, Enum):
    accessories = "Accessories"
    houses = "Houses"
    carriers = "Carriers"
    toys = "Toys"
    cleaning = "Cleaning & Maintenance"
    food="Food and Treats"
    beds= "Bed and Comfort"


class ProductBase(SQLModel):
    Product_Name: str
    Price: float
    Description: str
    Category: Categories 
    Image: str
    
class Product(ProductBase, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    Created_at: datetime = Field(default_factory= generate_timestamp)

class ProductDAO:
    def get_products():
        with Session(engine) as session:
            products = session.exec(select(Product)).all()
        return products   
    
    def create_product(new_product):
        with Session(engine) as session:
            session.add(new_product)
            session.commit()
        return {'status': '201 Created'}
