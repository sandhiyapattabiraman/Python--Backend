from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI,HTTPException
from .user_schema import UserCreate,UserLogin
from .user_service import UserService
from ..utils.auth import jwt_token_decrypt



user_router=APIRouter(prefix="/users")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

@user_router.post("/register")
def register_users(user:UserCreate):
    return UserService.create_user(user)

@user_router.post("/login")
def login_user(user_login:UserLogin):
    user= UserService.authenticate_user(user_login)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = user.get('access_token')
    if not access_token:
        raise HTTPException(status_code=500, detail="Error generating access token")

    return {"access_token": user["access_token"], "token_type": "bearer"}

@user_router.get("/me")
async def get_current_user(token: str=Depends(oauth2_scheme) ):
    payload = jwt_token_decrypt(token)
    user_id = payload.get("sub")
    user = UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.get("/profile")
def get_user_profile(token: str=Depends(oauth2_scheme)):
    payload = jwt_token_decrypt(token)
    user_id = payload.get("sub")
    user = UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
