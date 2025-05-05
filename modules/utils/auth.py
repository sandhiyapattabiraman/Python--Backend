from pydantic_settings import BaseSettings
from fastapi import Request,HTTPException, Depends
from sqlmodel import select
from datetime import datetime, timedelta  
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

Algorithm='HS256'
class Secret_key(BaseSettings):
    secret_key:str = "sandhiya"
    class Config:
        env_file = "venv"
secret_key=Secret_key()

def jwt_token_encrypt(new_user):
    payload={
        "sub": str(new_user.id),
        "username":new_user.username,
        "email":new_user.email,
        "exp": datetime.now() + timedelta(hours=1),
        "id": str(new_user.id)
    }
    token=jwt.encode(payload,secret_key.secret_key,algorithm=Algorithm)
    return token
def jwt_token_decrypt(jwt_token):
   try:
        payload = jwt.decode(jwt_token, secret_key.secret_key, algorithms=[Algorithm], options={"verify_exp": True})
        return payload
   except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
   except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def authenticate(request: Request):
    from modules.user .user_model import User, engine,Session 
    bearer_token=request.headers.get("Authorization")
    
    if not bearer_token or not bearer_token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    jwt_token=bearer_token.split(" ")[1]
    payload=jwt_token_decrypt(jwt_token)
    email=payload["email"]
    with Session(engine) as session:
        user=session.exec(select(User).where(User.email==email)).first()
        if not user:
            raise HTTPException(status_code=401,detail="Unauthorized")
        return user.id
    