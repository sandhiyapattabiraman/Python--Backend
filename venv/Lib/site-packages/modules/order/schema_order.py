from pydantic import BaseModel
from uuid import UUID

class OrderDetails(BaseModel):
    product_id: UUID
    product_image: str
    product_name: str
    product_price: float
    quantity: int
    name: str
    email: str
    address: str
    city: str
    state: str
    country: str
    pincode: str
    phoneNo: str
    payment_method: str