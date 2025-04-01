from sqlmodel import SQLModel, Field,select
from ..utils.database import Session,engine
from uuid import UUID




class User(SQLModel ,table=True):
    id: int = Field(default=None, primary_key=True)
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

    def get_user_byemail(email:str):
     with Session(engine) as session:
         users=session.exec(select(User).where(User.email==email)).first()
         return users

    def get_user_password_hash(email:str):
     with Session(engine) as session:
        users=session.exec(select(User).where(User.email==email)).first()
     return users.password_hash
 
    def get_user_byid(user_id:UUID):
     with Session(engine) as session:
        users=session.exec(select(User).where(User.id==user_id)).first()
     return users
     
