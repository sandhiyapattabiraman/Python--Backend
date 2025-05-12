from sqlmodel import SQLModel, Field, select
from uuid import UUID, uuid4
from ..utils.database import Session, engine
from ..product.model_product import Product



class Wishlist(SQLModel, table= True):
    id: UUID = Field(primary_key= True, default_factory= uuid4)
    user_id: UUID = Field(foreign_key="user.id")
    product_id: UUID = Field(foreign_key="product.id")
    
    
class WishlistDAO:
    def add_item(user_id, product_id):
         with Session(engine) as session:
             item = session.exec(select(Wishlist).where(Wishlist.user_id == user_id, Wishlist.product_id == product_id)).first()
             if item:
                session.delete(item)
                session.commit()
                return {"success": True, "message": "Product removed from wishlist"}
             item = Wishlist(user_id=user_id, product_id=product_id)
             session.add(item)
             session.commit()
             session.refresh(item)
         return {"success": True, "message": "Product added to wishlist"}
     
    def get_user_wishlist(user_id):
        with Session(engine) as session:
            statement = (
                select(Wishlist, Product)
                .join(Product, Wishlist.product_id == Product.id)
                .where(Wishlist.user_id == user_id)
            )
            results = session.exec(statement).all()
            wishlist_products = []
            for wishlist, product in results:
                wishlist_products.append({
                    "product_id": product.id,
                    "name": product.Product_Name,
                    "price": product.Price,
                    "image": product.Image
                })
            return wishlist_products
        
    def remove_item(user_id, product_id):
        with Session(engine) as session: 
            item = session.exec(select(Wishlist).where(Wishlist.user_id == user_id, Wishlist.product_id == product_id)).first()
            if item:
                session.delete(item)
                session.commit()
                return True
            return None