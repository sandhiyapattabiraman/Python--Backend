from fastapi import APIRouter
from fastapi import Depends, FastAPI,HTTPException, status
from .user_schema import UserCreate,UserLogin
from .user_service import UserService
from ..utils.auth import  authenticate
from uuid import UUID


user_router=APIRouter(prefix="/users")

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


@user_router.get("/current-user")
def current_user(current_user: UUID = Depends(authenticate)):
    user = UserService.get_username(current_user)
    return {'username': user.username}
    

