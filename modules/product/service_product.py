from .model_product import ProductDAO , Product
from fastapi import HTTPException
from ..utils.database import Session, engine
from sqlmodel import select


class ProductService:
    def get_products():
        return ProductDAO.get_products()
    
    def post_products(create_product):
        new_product = Product(**create_product.model_dump(),)
        return ProductDAO.create_product(new_product)
    
    def delete_product(product_id):
        deleted = ProductDAO.delete_by_id(product_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product deleted successfully"}
    
    def get_category_product(category_name):
        category_id = ProductDAO.get_category_id(category_name)
        with Session(engine) as session:
            products = session.exec(select(Product).where(Product.category_id == category_id)).all()
        return products