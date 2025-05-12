from fastapi import APIRouter
from .schema_category import CreateCategory
from .service_category import CategoryService
from uuid import UUID

category_router = APIRouter(prefix="/category")

@category_router.post("/create_category")
def create_category(category: CreateCategory):
    return CategoryService.create_category(category)

@category_router.get("/")
def get_category():
    return CategoryService.get_category()

@category_router.delete("/")
def delete_category(id: UUID):
    return CategoryService.delete_category(id)