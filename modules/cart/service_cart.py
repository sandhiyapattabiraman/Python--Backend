from sqlmodel import select
from .model_cart import CartDAO, UserCart, cart
from ..utils.database import Session, engine
from uuid import UUID

class CartService:
    def get_items(user_id):
        return CartDAO.get_cart(user_id)
    
    def add_item(userid, item):
        with Session(engine) as session:
            user_cart_obj = session.exec(select(UserCart).where(UserCart.user_id == userid)).first()

            if not user_cart_obj:
                user_cart_id = CartDAO.create_userCart(userid)
            else:
                user_cart_id = user_cart_obj.id

            existing_item = session.exec(
                select(cart).where(cart.cart_id == user_cart_id, cart.product_id == item.product_id)
            ).first()

            if existing_item:
                existing_item.quantity += item.quantity
                session.add(existing_item) 
                session.commit()
                session.refresh(existing_item)
                return {"success": True, "message":"Quantity increased"}

            else:
                cart_item = cart(
                    user_id=userid,
                    product_id=item.product_id,
                    cart_id=user_cart_id,
                    quantity=item.quantity
                )
                session.add(cart_item)
                session.commit()
                session.refresh(cart_item)
                return {"success": True, "message": "Product added to cart"}
            
    def remove_item(user_id, product_id):
        return CartDAO.remove_cart_item(user_id, product_id)

    def update_quantity(user_id: UUID, product_id: UUID, change: int):
        return CartDAO.update_quantity(user_id, product_id, change)
