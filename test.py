import pytest
from fastapi.testclient import TestClient
from server import app
from models import DishStatus
import services

client = TestClient(app)

@pytest.fixture(autouse=True)
async def mock_services(monkeypatch):
    async def mock_is_valid_dish_id(dish_id):
        return dish_id in [1, 2, 3]
    
    async def mock_create_order(dish_ids):
        return 1
    
    async def mock_update_dish_status(order_id, dish_id, status):
        return True
    
    monkeypatch.setattr(services, "is_valid_dish_id", mock_is_valid_dish_id)
    monkeypatch.setattr(services, "create_order", mock_create_order)
    monkeypatch.setattr(services, "update_dish_status", mock_update_dish_status)

class TestCreateOrder:
    def test_create_order_success(self):
        response = client.post("/orders", json={"dish_ids": [1, 2, 3]})
        assert response.status_code == 200
        assert response.json() == {"order_id": 1}

    def test_create_order_invalid_dish_id(self):
        response = client.post("/orders", json={"dish_ids": [1, 999]})
        assert response.status_code == 404
        assert "Dish ID 999 not found" in response.json()["detail"]

    def test_create_order_invalid_request(self):
        response = client.post("/orders", json={"wrong_field": []})
        assert response.status_code == 422

class TestUpdateDishStatus:
    def test_update_dish_status_success(self):
        request = {
            "order_id": 1,
            "dish_id": 1,
            "status": "Preparing"
        }
        response = client.post("/kitchen/update_dish", json=request)
        assert response.status_code == 200
        assert response.json() == {"message": "Dish status updated"}

    def test_update_dish_status_invalid_status(self):
        request = {
            "order_id": 1,
            "dish_id": 1,
            "status": "INVALID_STATUS"
        }
        response = client.post("/kitchen/update_dish", json=request)
        assert response.status_code == 400
        assert "Invalid status" in response.json()["detail"]

    def test_update_dish_status_not_found(self, monkeypatch):
        async def mock_update_dish_status(order_id, dish_id, status):
            return False
        
        monkeypatch.setattr(services, "update_dish_status", mock_update_dish_status)
        request = {
            "order_id": 999,
            "dish_id": 999,
            "status": "Preparing"
        }
        response = client.post("/kitchen/update_dish", json=request)
        assert response.status_code == 404
        assert "Order or dish not found" in response.json()["detail"]