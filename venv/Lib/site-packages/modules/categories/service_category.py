from .model_category import Categories, CategoryDAO
from ..utils.database import Session, engine
from sqlmodel import select
from fastapi import HTTPException

class CategoryService:
    
    def create_category(create_category):
        with Session(engine) as session:
            statement = select(Categories).where(Categories.name == create_category.name)
            result = session.exec(statement).first()

        if result:
            return{"message":"Category already exists!"}
        new_category = Categories(**create_category.model_dump(),)
        return CategoryDAO.new_category(new_category)
    
    def get_category():
        return CategoryDAO.get_category()
    
    def delete_category(id):
        deleted = CategoryDAO.delete_by_id(id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Category deleted successfully"}