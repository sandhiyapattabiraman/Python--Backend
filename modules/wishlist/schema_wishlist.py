from pydantic import BaseModel
from uuid import UUID

class AddItem(BaseModel):
    product_id: UUID