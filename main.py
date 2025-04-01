from fastapi import FastAPI
from contextlib import asynccontextmanager
from modules.utils.database import create_db_and_tables
from modules.product.controller_product import product_router
from modules.user.user_controller import user_router

app = FastAPI()

@asynccontextmanager
async def lifespan(app):
       create_db_and_tables()
       yield
       
app = FastAPI(title="project", lifespan=lifespan)

app.include_router(router=user_router)
app.include_router(router = product_router)

@app.get("/")
def initial_route(): 
    return {"message" : "Hello sandhiya"}


