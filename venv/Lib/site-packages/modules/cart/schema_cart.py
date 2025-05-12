from pydantic import BaseModel
from uuid import UUID

class AddItem(BaseModel):
    product_id: UUID
    quantity: int
    
class QuantityUpdate(BaseModel):
    product_id: UUID
    change: int