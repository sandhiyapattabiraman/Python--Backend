from fastapi import APIRouter, Request, Depends, Body
from .service_cart import CartService
from .schema_cart import AddItem, QuantityUpdate
from ..utils.auth import authenticate
from fastapi import HTTPException
from uuid import UUID

cart_router = APIRouter(prefix="/cart")

@cart_router.get("/")
def get_cart_items(request: Request):
    user_id = authenticate(request)
    return CartService.get_items(user_id)

@cart_router.post("/addToCart")
def add_to_cart(request: Request, item: AddItem ):
    user_id= authenticate(request)
    return CartService.add_item(user_id, item)

@cart_router.delete("/deleteItem/{product_id}")
def remove_cart_item(product_id: UUID, user_id: UUID = Depends(authenticate)):
    result = CartService.remove_item(user_id, product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    return result

@cart_router.put("/update_quantity/{product_id}")
def update_quantity(data: QuantityUpdate, user_id: UUID = Depends(authenticate)):
    result = CartService.update_quantity(user_id, data.product_id, data.change)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found or invalid quantity")
    return result

