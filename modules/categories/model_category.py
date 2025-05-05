from sqlmodel import SQLModel, Field, select
from uuid import UUID, uuid4
from ..utils.database import Session, engine

class Categories(SQLModel, table = True):
    id: UUID = Field(primary_key= True, default_factory=uuid4)
    name: str
    image: str
    
    
class CategoryDAO():
    
    def new_category(new):
        with Session(engine) as session:
            session.add(new)
            session.commit()
        return {'message': 'Category Created Successfully'}
    
    def get_category():
        with Session(engine) as session:
            categories = session.exec(select(Categories)).all()
        return categories
    
    def delete_by_id(category_id):
        with Session(engine) as session:
            category = session.get(Categories, category_id)
            if not category:
                return False
            session.delete(category)
            session.commit()
            return True