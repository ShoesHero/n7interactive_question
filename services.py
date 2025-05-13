from models import *
from database import menu, orders, lock
from typing import List
import asyncio

async def get_menu() -> List[Dish]:
    return list(menu.values())

async def create_order(dish_ids: List[int]) -> int:
    global orders
    from database import order_counter
    async with lock:
        order_id = order_counter
        order_counter += 1
        ordered_dishes = [OrderedDish(dish_id=d) for d in dish_ids]
        orders[order_id] = Order(id=order_id, dish_items=ordered_dishes)
        return order_id

async def get_order(order_id: int) -> Order | None:
    async with lock:
        return orders.get(order_id)

async def update_dish_status(order_id: int, dish_id: int, new_status: DishStatus) -> bool:
    async with lock:
        order = orders.get(order_id)
        if not order:
            return False
        for dish in order.dish_items:
            if dish.dish_id == dish_id:
                dish.status = new_status
                break
        await update_order_status(order)
        return True

async def update_order_status(order: Order):
    statuses = [d.status for d in order.dish_items]
    if all(s == DishStatus.ready for s in statuses):
        order.status = OrderStatus.completed
    else:
        order.status = OrderStatus.pending

async def get_pending_orders() -> List[Order]:
    async with lock:
        return [o for o in orders.values() if o.status != OrderStatus.completed]

async def is_valid_dish_id(dish_id: int) -> bool:
    return dish_id in menu
