from fastapi import APIRouter,  Depends, HTTPException
from ..utils.auth import authenticate
from .schema_order import OrderDetails
from uuid import UUID
from .service_order import OrderService
from .model_order import Address, Order
from typing import List




order_router = APIRouter(prefix= "/order")

@order_router.post("/placeOrder")
def place_order(details: List[OrderDetails], user_id: UUID = Depends(authenticate)):
    print(details)
    try:
        results = []

        for item in details:
            address_id = OrderService.get_address_id(user_id)

            if address_id is None:
                address_details = Address(
                    user_id=user_id,
                    name=item.name,
                    email=item.email,
                    address=item.address,
                    city=item.city,
                    state=item.state,
                    country=item.country,
                    pincode=item.pincode,
                    phoneNo=item.phoneNo
                )
                address_id = OrderService.add_address(address_details)

            new_order = Order(
                user_id=user_id,
                product_id=item.product_id,
                product_image=item.product_image,
                product_name=item.product_name,
                product_price=float(item.product_price),
                quantity=item.quantity,
                address_id=address_id,
                payment_method=item.payment_method
            )

            result = OrderService.place_order(new_order)
            results.append(result)
        OrderService.clear_cart(user_id)
        return results

    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    

@order_router.get("/getOrders")
def get_orders(user_id: UUID = Depends(authenticate)):
    try:
        orders = OrderService.get_user_orders(user_id)
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found for this user.")
        return orders
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@order_router.get("/bestseller")
def best_seller():
    try:
        data = OrderService.get_products()
        return data
    except Exception as e:
        return {"error": str(e)}