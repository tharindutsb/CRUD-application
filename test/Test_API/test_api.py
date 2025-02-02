import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_intern():
    response = client.post("/interns/", json={
        "name": "Sampath",
        "address": "Homagama",
        "email": "sampath@example.com",
        "contact_no": "0716542080"
    })
    assert response.status_code == 200
    assert "intern_id" in response.json()

def test_get_intern():
    response = client.get("/interns/0001")
    assert response.status_code == 200
    assert response.json()["name"] == "Sampath"

def test_update_intern():
    response = client.put("/interns/0001", json={
        "name": "Updated Sampath",
        "address": "New Address",
        "email": "updated@example.com",
        "contact_no": "0716542081"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Sampath"

def test_delete_intern():
    response = client.delete("/interns/0001")
    assert response.status_code == 200
    assert "message" in response.json()
