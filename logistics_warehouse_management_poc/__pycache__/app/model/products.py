from pydantic import BaseModel
from typing import Optional
from datetime import date

class Product(BaseModel):
    id : str
    name : str
    price : float
    stock : int
    category : str
    description : Optional[str] = None
    expiry_date : date

class UpdateProduct(BaseModel):
    name : str
    stock: Optional[int] =None
    price : Optional[float] = None
    description : Optional[str] = None

class GetProduct(BaseModel):
    id : Optional[str] = None
    name : Optional[str] = None

