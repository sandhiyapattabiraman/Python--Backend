from sqlmodel import SQLModel, Field,select
from ..utils.database import Session,engine
from uuid import UUID, uuid4




class User(SQLModel ,table=True):
    id: UUID = Field( primary_key=True, default_factory=uuid4)
    username: str
    email: str = Field(unique=True)
    password_hash: str

__all__=[User]    

class UserDao:

    def create_users(new_user):
        with Session(engine) as session:
         session.add(new_user)
         session.commit()
         session.refresh(new_user)
        return new_user

    def get_user_byemail(email):
     with Session(engine) as session:
         users=session.exec(select(User).where(User.email==email)).first()
         return users

    def get_user_password_hash(email:str):
     with Session(engine) as session:
        users=session.exec(select(User).where(User.email==email)).first()
     return users.password_hash
 
    
     
