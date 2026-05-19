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
def create_test_struct(clear_bd):
    structs = []
    for i in range(1, 41):
        response = client.post("/struct", json={
            "number_of_tooth": i,
            "hight": i * 1.5,
            "name": f"name_{i}",
            "created_at": str(datetime.today().date()),
            "birth_date": str(datetime.today().date())
        })
        structs.append(response.json())
    return structs


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

    def test_post_bad_url(self,clear_bd):
        struct_data = {
            "number_of_tooth": 5,
            "hight": 1.45,
            "name": "gleb",
            "created_at": "2026-05-11",
            "birth_date": "2000-01-15"
        }
        response = client.post("/struct/2", json=struct_data)
        assert response.status_code == 405
        assert client.get("/struct/").json() == { "detail": "No structures found" }

    def test_create_bad_struct(self,clear_bd):
        bad_struct_data  = {
            "name": "Belyi",
            "surname": "Ivanov",
            "age": 19
        }
        response = client.post("/struct/", json = bad_struct_data)
        assert response.status_code == 422
        assert client.get("/struct/").json() == { "detail": "No structures found" }


class TestGetStruct:
    def test_get_success(self, create_test_struct):
        old_data = create_test_struct[0:41]
        response = client.get("/struct/23")
        assert response.status_code == 200
        assert old_data == create_test_struct

    def test_get_all_struct_success(self, create_test_struct):
        response = client.get("/struct/?limit=10&offset=10")
        assert response.status_code == 200
        data = response.json()
        assert data["data"][0]["number_of_tooth"] == 11
        assert data["data"][len ( data ["data"] ) - 1]["number_of_tooth"] == 20
        assert data["next_offset"] == 20

    def test_get_all_small_structure(self, create_test_struct):
        response = client.get("/struct/?limit=10")
        assert response.status_code == 200
        assert len(response.json()["data"]) <= response.json()["total"]

    def test_get_all_with_pagination(self, create_test_struct):
        limit = 5
        offset = 5
        response = client.get(f"/struct/?limit={limit}&offset={offset}")
        data = response.json()['data']
        for struct in data:
            value = struct["number_of_tooth"]
            assert offset < value < offset + limit + 1


class TestPutStruct:
    def test_put_success(self,create_test_struct):
        new_data = {
            "number_of_tooth": 5,
            "hight": 1.45,
            "name": "gleb",
            "created_at": "2026-05-11",
            "birth_date": "2000-01-15"
        }
        response = client.put(f"/struct/3", json=new_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Structure updated"
        assert data["data"]["number_of_tooth"] == 5
        assert data["data"]["hight"] == 1.45
        assert data["data"]["name"] == "gleb"
        assert data["data"]["created_at"] == "2026-05-11"
        assert data["data"]["birth_date"] == "2000-01-15"

    def test_put_bad_struct(self, create_test_struct):
        new_data = {
            "number_of_tootooth": 5,
            "hight": 1.45,
            "name": "gleb",
            "created_at": "2026-05-11",
            "birth_date": "2000-01-15"
        }
        old_data = create_test_struct[3]
        response = client.put(f"/struct/{create_test_struct[3]}", json=new_data)
        assert response.status_code == 422
        assert create_test_struct[3] == old_data

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

    def test_put_bad_url(self,create_test_struct):
        new_data = {
            "number_of_tooth": 5,
            "hight": 1.45,
            "name": "gleb",
            "created_at": "2026-05-11",
            "birth_date": "2000-01-15"
        }
        old_data = list(create_test_struct[1:6])
        response = client.put(f"/struct/", json=new_data)
        assert response.status_code == 405
        assert create_test_struct[1:6] == old_data


class TestPatchStruct:
    def test_patch_success(self, create_test_struct):
        new_data = {
            "number_of_tooth": 543,
            "hight": 1.4335,
        }
        response = client.patch("/struct/4", json=new_data)
        assert response.status_code == 200
        update_data = client.get("/struct/").json()
        assert update_data["data"][3]["number_of_tooth"] == 543
        assert update_data["data"][3]["hight"] == 1.4335

    def test_patch_bad_url(self, create_test_struct):
        new_data = {
            "number_of_tooth": 543,
            "hight": 1.4335,
        }
        old_data = create_test_struct[1:6]
        response = client.patch("/struct/", json= new_data)
        assert response.status_code == 405
        assert create_test_struct[1:6] == old_data


    def test_patch_not_found(self, create_test_struct):
        new_data = {
            "number_of_tooth": 543,
            "hight": 1.4335,
        }
        response = client.patch("/struct/999", json=new_data)
        assert response.status_code == 404

    def test_patch_not_field(self,clear_bd,create_test_struct):
        new_data = {
            "point": 3
        }
        response = client.patch(f"/struct/4", json=new_data)
        assert response.status_code == 400


class TestDeleteStruct:
    def test_delete_success(self,create_test_struct):
        response = client.delete("/struct/3")
        deleted_data = response.json()['data']
        assert response.status_code == 200
        assert deleted_data not in create_test_struct


    def test_delete_not_found(self,clear_bd):
        response = client.delete("/struct/999")
        assert response.status_code == 404

    def test_delete_bad_url(self, create_test_struct):
        old_data = create_test_struct[1:6]
        response = client.delete("/struct")
        assert response.status_code == 405
        assert old_data == create_test_struct[1:6]
