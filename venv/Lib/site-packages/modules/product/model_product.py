from sqlmodel import SQLModel, Field, select
from ..utils.database import Session, engine
from uuid import uuid4, UUID
from datetime import datetime, timezone
from ..categories.model_category import Categories

def generate_timestamp():
    return datetime.now(timezone.utc)




class ProductBase(SQLModel):
    Product_Name: str
    Price: float
    Description: str 
    category_id: UUID = Field(foreign_key="categories.id")
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
        return {'message': 'Product Created Successfully'}
    
    def delete_by_id(product_id):
        with Session(engine) as session:
            product = session.get(Product, product_id)
            if not product:
                return False
            session.delete(product)
            session.commit()
            return True
    
    def get_category_id(category_name):
        with Session(engine) as session:
            category_query = select(Categories).where(Categories.name == category_name)
            category = session.exec(category_query).first()

        if not category:
            return {"error": "Category not found"}
        
        return category.id