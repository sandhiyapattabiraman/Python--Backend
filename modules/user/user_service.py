from .user_schema import UserCreate,UserLogin
from .user_model import User,UserDao
import bcrypt
from ..utils.auth import jwt_token_encrypt
from fastapi import HTTPException
from uuid import UUID
from ..utils .auth import jwt_token_encrypt



class UserService():

   def hash_password(password: str) -> str:
     salt = bcrypt.gensalt()
     hashed_password = bcrypt.hashpw(password.encode(), salt)
     return hashed_password.decode()
 
   def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

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


   def authenticate_user(user_login:UserLogin):
     user= UserDao.get_user_byemail(user_login.email)
     gethashpasword=UserDao.get_user_password_hash(user_login.email)
     if not user or not UserService.verify_password(user_login.password,gethashpasword):
        raise HTTPException(status_code=401, detail="Invalid credentials")
     token = jwt_token_encrypt(user)
     return {"access_token": token, "token_type": "bearer"}
   def get_user_by_id(user_id:UUID):
      return UserDao.get_user_byid(user_id)
