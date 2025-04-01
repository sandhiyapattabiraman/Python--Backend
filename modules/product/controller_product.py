from fastapi import APIRouter
from .service_product import ProductService
from .schema_product import CreateProduct


product_router= APIRouter(prefix="/products")

@product_router.get("/")
def get_products():
    return ProductService.get_products()

@product_router.post("/")
def create_product(create_product: CreateProduct):
    return ProductService.post_products(create_product)

@product_router.delete("/")
def delete_product():
    pass