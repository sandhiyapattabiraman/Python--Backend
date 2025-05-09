from sqlmodel import SQLModel, Field, select, func
from uuid import uuid4, UUID
from datetime import datetime, timezone
from ..utils.database import Session, engine
from sqlmodel import delete
from ..cart.model_cart import cart
from ..product.model_product import Product


def generate_timestamp():
    return datetime.now(timezone.utc)

class Order(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    user_id: UUID =Field(foreign_key='user.id')
    product_id: UUID = Field(foreign_key='product.id')
    product_image: str
    product_name: str
    product_price: float
    quantity: int
    address_id: UUID = Field(foreign_key='address.id')
    payment_method: str
    created_at: datetime = Field(default_factory=generate_timestamp)
    
    
class Address(SQLModel, table = True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    user_id: UUID = Field(foreign_key='user.id')
    name: str
    email: str
    address: str
    city: str
    state: str
    country: str
    pincode: str
    phoneNo: str



class OrderDAO:
    def get_address_id(user_id):
        with Session(engine) as session:
            detail = session.exec(select(Address).where(Address.user_id == user_id)).first()
            
            if detail:
                return detail.id
        return None

    def add_address(details):
        with Session(engine) as session:
            session.add(details)
            session.commit()
            session.refresh(details)
            return details.id

    def place_order(new_order):
        with Session(engine) as session:
            session.add(new_order)
            session.commit()
            session.refresh(new_order)
        return{ "success": True ,"message": "Order placed successfully"}

    def get_orders_by_user(user_id):
        with Session(engine) as session:
            orders = session.exec(select(Order).where(Order.user_id == user_id)).all()
            return orders

    def clear_cart(user_id):
        with Session(engine) as session:
            session.exec(delete(cart).where(cart.user_id == user_id))
            session.commit()

    def most_sold():
        with Session(engine) as session:
           statement = (
            select(
                Order.product_id,
                Order.product_name,
                Product.Price,
                Product.Description,
                Order.product_image,
                func.sum(Order.quantity).label("total_sold")
            )
            .join(Product, Product.id == Order.product_id)
            .group_by(Order.product_id)
            .order_by(func.sum(Order.quantity).desc())
            .limit(10)
        )
        results = session.exec(statement).all()

        bestsellers = []
        for row in results:
            bestsellers.append({
                "product_id": row.product_id,
                "name": row.product_name,
                "description": row.Description,
                "price": row.Price,
                "image_url": row.product_image,
                "total_sold": row.total_sold
            })

        return bestsellers
        
