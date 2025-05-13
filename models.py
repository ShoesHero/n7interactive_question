from enum import Enum
from pydantic import BaseModel
from typing import List

class DishStatus(str, Enum):
    preparing = "Preparing"
    ready = "Ready"

class OrderStatus(str, Enum):
    pending = "Pending"
    completed = "Completed"

class Dish(BaseModel):
    id: int
    name: str
    price: float

class OrderedDish(BaseModel):
    dish_id: int
    status: DishStatus = DishStatus.preparing

class Order(BaseModel):
    id: int
    dish_items: List[OrderedDish]
    status: OrderStatus = OrderStatus.pending
