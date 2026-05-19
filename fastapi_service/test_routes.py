from http.client import responses

import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from main import app
from database import db

client = TestClient(app)

@pytest.fixture
def clear_bd():
    db.clear()
    yield
    db.clear()

@pytest.fixture
def five_struct(clear_bd):
    ids = []
    for i in range(1, 6):
        response = client.post("/struct", json={
            "number_of_tooth": i*3,
            "hight": i*1.5,
            "name": f"name_{i}",
            "created_at": str(datetime.today().date()),
            "birth_date": str(datetime.today().date())
        })
        ids.append(response.json()["id"])
    return ids

class TestPostStruct:
    def test_create_success(self, clear_bd):
        struct_data = {
            "number_of_tooth": 5,
            "hight": 1.45,
            "name": "gleb",
            "created_at": "2026-05-11",
            "birth_date": "2000-01-15"
        }
        response = client.post("/struct", json=struct_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Struct created"
        assert "id" in data

class TestPutStruct:
    def test_put_success(self,clear_bd, five_struct):
        new_data = {
            "number_of_tooth": 5,
            "hight": 1.45,
            "name": "gleb",
            "created_at": "2026-05-11",
            "birth_date": "2000-01-15"
        }
        response = client.put(f"/struct/{five_struct[0]}", json=new_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Structure updated"
        assert data["data"]["number_of_tooth"] == 5
        assert data["data"]["hight"] == 1.45
        assert data["data"]["name"] == "gleb"
        assert data["data"]["created_at"] == "2026-05-11"
        assert data["data"]["birth_date"] == "2000-01-15"

    def test_put_not_found(self, clear_bd):
        new_data = {
            "number_of_tooth": 5,
            "hight": 1.45,
            "name": "gleb",
            "created_at": "2026-05-11",
            "birth_date": "2000-01-15"
        }
        response = client.put(f"/struct/999", json=new_data)
        assert response.status_code == 404

class TestPatchStruct:
    def test_patch_success(self, clear_bd,five_struct):
        new_data = {
            "number_of_tooth": 543,
            "hight": 1.4335,
        }
        response = client.patch(f"/struct/{five_struct[0]}", json=new_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Structure changed"
        assert data["data"]["number_of_tooth"] == 543
        assert data["data"]["hight"] == 1.4335

    def test_patch_not_found(self,clear_bd,five_struct):
        new_data = {
            "number_of_tooth": 543,
            "hight": 1.4335,
        }
        response = client.patch("/struct/999", json=new_data)
        assert response.status_code == 404

    def test_patch_not_field(self,clear_bd,five_struct):
        new_data = {
            "point": 3
        }
        response = client.patch(f"/struct/{five_struct[0]}", json=new_data)
        assert response.status_code == 400

class TestDeleteStruct:
    def test_delete_success(self,clear_bd, five_struct):
        delete_id = five_struct[2]
        response = client.delete("/struct/3")
        assert response.status_code == 200
        response = client.get("/struct")
        data = response.json()
        assert len(data["data"]) == 4

    def test_delete_not_found(self,clear_bd):
        response = client.delete("/struct/999")
        assert response.status_code == 404


