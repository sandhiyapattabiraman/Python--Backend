from fastapi import APIRouter, Depends, HTTPException, Request
from .schema_wishlist import AddItem
from ..utils.auth import authenticate
from uuid import UUID
from .service_wishlist import WishlistService


wishlist_router= APIRouter(prefix='/wishlist')

@wishlist_router.get("/")
def get_wishlist(user_id: UUID = Depends(authenticate)):
    items = WishlistService.get_items(user_id)
    if not items:
        raise HTTPException(status_code=404, detail="No items found in wishlist")
    return {"wishlist": items}

@wishlist_router.post("/addItem")
def add_wishlist(product_id: AddItem, user_id:UUID= Depends(authenticate)):
    result = WishlistService.add_item(user_id, product_id.product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    return result 

@wishlist_router.delete("/removeItem/{product_id}")
def remove_item(product_id: UUID, user_id: UUID = Depends(authenticate)):
    result = WishlistService.remove_item(user_id, product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found in wishlist")
    return {"success": True, "message": "Item removed from wishlist"}