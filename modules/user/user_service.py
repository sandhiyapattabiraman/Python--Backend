from .user_schema import UserCreate
from .user_model import User,UserDao
import bcrypt
from ..utils.auth import jwt_token_encrypt
from fastapi import HTTPException
from ..utils.database import Session,engine
from sqlmodel import select





class UserService():

   def hash_password(password: str) -> str:
     salt = bcrypt.gensalt()
     hashed_password = bcrypt.hashpw(password.encode(), salt)
     return hashed_password.decode()

   def verify_password(plain_password: str, hashed_password: str) -> bool:
      result = bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
      print("Password match:", result)
      return result
    

   def create_user(user_create:UserCreate):
    hashed_password = UserService.hash_password(user_create.password)  

    new_user=User(   
        username=user_create.username,
        email=user_create.email,
        password_hash=hashed_password
        )
    new_users=UserDao.create_users(new_user)
    token=jwt_token_encrypt(new_users)
    return {"username":new_user.username,"email":new_user.email,"token":token}


   def authenticate_user(user_login):
    user = UserDao.get_user_byemail(user_login.email)
    
    if not user:
        return None 

    if not UserService.verify_password(user_login.password, user.password_hash):
        return None  

    token = jwt_token_encrypt(user)
    print(token)
    return {"access_token": token, "token_type": "bearer"}

   
   def get_username(user_id):
     with Session(engine) as session:
       user = session.exec(select(User).where(User.id == user_id)).first()
       return user
