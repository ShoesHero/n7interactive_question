from fastapi import FastAPI, HTTPException
from models import DishStatus
from schemas import *
import services

app = FastAPI(title="order system")


@app.get("/menu", description="Get the menu")
async def read_menu():
    return await services.get_menu()

@app.post("/orders", response_model=OrderResponse, description="Create an order")
async def create_order(req: OrderRequest):
    for dish_id in req.dish_ids:
        if not await services.is_valid_dish_id(dish_id):
            raise HTTPException(status_code=404, detail=f"Dish ID {dish_id} not found")
    order_id = await services.create_order(req.dish_ids)
    return {"order_id": order_id}

@app.get("/orders/{order_id}", description="Get an order by ID")
async def get_order(order_id: int):
    order = await services.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found nya~")
    return order

@app.post("/kitchen/update_dish", description="Update the status of a dish")
async def update_dish_status(req: UpdateDishStatusRequest):
    try:
        status = DishStatus(req.status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")
    ok = await services.update_dish_status(req.order_id, req.dish_id, status)
    if not ok:
        raise HTTPException(status_code=404, detail="Order or dish not found")
    return {"message": "Dish status updated"}

@app.get("/kitchen/pending_orders", description="Get all pending orders")
async def pending_orders():
    return await services.get_pending_orders()