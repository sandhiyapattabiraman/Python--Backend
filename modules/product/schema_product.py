from pydantic import BaseModel 



class CreateProduct(BaseModel):
    Product_Name: str
    Price: float
    Description: str
    Category: str
    Image: str
    