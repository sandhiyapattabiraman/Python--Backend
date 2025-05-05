from fastapi import APIRouter, HTTPException
from .service_product import ProductService
from .schema_product import CreateProduct
from uuid import UUID
from ..utils.database import Session, engine
from sqlmodel import select
from ..categories.model_category import Categories
from .model_product import Product

product_router= APIRouter(prefix="/products")

@product_router.get("/")
def get_products():
    return ProductService.get_products()

@product_router.post("/create")
def create_product(create_product: CreateProduct):
    with Session(engine) as session:
        category_name = create_product.Category
        
        category_query = select(Categories).where(Categories.name == category_name)
        category = session.exec(category_query).first()

        if not category:
            return {"error": "Category not found"}
        
        product = Product(
            Product_Name=create_product.Product_Name,
            Price=create_product.Price,
            Description=create_product.Description,
            category_id=category.id,
            Image=create_product.Image
        )
    return ProductService.post_products(product)

@product_router.delete("/delete")
def delete_product(product_id: UUID):
    return ProductService.delete_product(product_id)

@product_router.get("/get")
def get_product_by_category(categoryname: str):
    return ProductService.get_category_product(categoryname)
        

@product_router.get("/search")
def search_products(query: str):
    try:
        with Session(engine) as session:
            search_query = select(Product).where(Product.Product_Name.ilike(f"%{query}%"))
            

            products = session.exec(search_query).all()

            if not products:
                raise HTTPException(status_code=404, detail="No products found matching the query.")
            
            return products
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
