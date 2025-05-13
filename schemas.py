from typing import List
from pydantic import BaseModel

class OrderRequest(BaseModel):
    dish_ids: List[int]

class OrderResponse(BaseModel):
    order_id: int

class UpdateDishStatusRequest(BaseModel):
    order_id: int
    dish_id: int
    status: str
