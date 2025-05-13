from typing import Dict
from models import Dish, Order
import asyncio

menu: Dict[int, Dish] = {
    1: Dish(id=1, name="Fried Rice", price=10.99),
    2: Dish(id=2, name="Dumplings", price=12.99),
    3: Dish(id=3, name="Kung Pao Chicken", price=18.99),
    4: Dish(id=4, name="Lee's Special", price=9999999.99)
}

orders: Dict[int, Order] = {}
order_counter = 1

lock = asyncio.Lock()
