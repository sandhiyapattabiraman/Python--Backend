from fastapi import FastAPI
from contextlib import asynccontextmanager
from modules.utils.database import create_db_and_tables
from modules.product.controller_product import product_router
from modules.user.user_controller import user_router
from modules.cart.controller_cart import cart_router
from modules.categories.controller_category import category_router
from modules.wishlist.controller_wishlist import wishlist_router
from modules.order.controller_order import order_router
from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def lifespan(app):
       create_db_and_tables()
       yield
 
app = FastAPI(title="project", lifespan=lifespan)     

origins = [
    "http://localhost:5501",
    "https://pet-world04.netlify.app/",
]

app.add_middleware(
    CORSMiddleware,
<<<<<<< HEAD
    allow_origins=origins,  
=======
    allow_origins=["*"],  
>>>>>>> b90e642fefa9663549725e57453344acf8900d66
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(router=user_router)
app.include_router(router = product_router)
app.include_router(router=cart_router)
app.include_router(router= category_router)
app.include_router(router= wishlist_router)
app.include_router(router= order_router)

@app.get("/")
def initial_route(): 
    return {"message" : "Hello sandhiya"}


