from sqlmodel import SQLModel, Field, select
from uuid import uuid4, UUID
from ..utils.database import Session, engine
from ..product.model_product import Product

class CartBase(SQLModel):
    user_id: UUID
    product_id: UUID
    
    
class cart(CartBase, table= True):
    id: UUID =Field(primary_key=True, default_factory=uuid4)
    cart_id: UUID = Field(foreign_key='usercart.id')
    quantity: int
    
class UserCart(SQLModel, table=True):
    id: UUID =Field(primary_key=True, default_factory=uuid4)
    user_id: UUID =Field(foreign_key='user.id')
    
class CartDAO:
    def get_cart(user_id):
        with Session(engine) as session:
            items = session.exec(
                select(cart).where(cart.user_id == user_id)
            ).all()
        if not items:
            return {"message": "No items found in the cart"}
        
        result = []
        total_price = 0
        for item in items:
            product = session.exec(select(Product).where(Product.id == item.product_id)).first()
            if product:
                item_total = item.quantity * product.Price
                total_price += item_total
                result.append({
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "product_name": product.Product_Name,
                    "product_image": product.Image,
                    "price": item_total,
                    
                })

        return {
            "cart_items": result,
            "total_price": total_price
        }
    
    def create_userCart(userid):
        with Session(engine) as session:
            user_cart = UserCart(id=uuid4(), user_id=userid)
            session.add(user_cart)
            session.commit()
            session.refresh(user_cart)
        return user_cart.id
        
    def remove_cart_item(user_id, product_id):
        with Session(engine) as session:
            item = session.exec(
                select(cart).where(cart.user_id == user_id, cart.product_id == product_id)
            ).first()

            if not item:
                return None
            
            session.delete(item)
            session.commit()
        return {"message": "Item removed from cart"}

    def update_quantity(user_id: UUID, product_id: UUID, change: int):
        with Session(engine) as session:
            item = session.exec(
                select(cart).where(cart.user_id == user_id, cart.product_id == product_id)
            ).first()

            if not item:
                return None

            new_quantity = item.quantity + change
            if new_quantity < 1:
                return None 

            item.quantity = new_quantity
            session.add(item)
            session.commit()
            session.refresh(item)
        return {"message": "Quantity updated successfully"}
