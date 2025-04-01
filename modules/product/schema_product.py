from pydantic import BaseModel 
from enum import Enum

class Categories(str, Enum):
    accessories = "Accessories"
    houses = "Houses"
    carriers = "Carriers"
    toys = "Toys"
    cleaning = "Cleaning & Maintenance"
    food="Food and Treats"
    beds= "Bed and Comfort"

class CreateProduct(BaseModel):
    Product_Name: str
    Price: float
    Description: str
    Category: Categories 
    Image: str
    