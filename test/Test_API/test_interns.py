import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_intern():
    response = client.post("/interns/", json={
        "name": "Tharindu",
        "address": "198,Yatawatura Rd,Malagala Padukka",
        "email": "tharindutsb@gmail.com",
        "contact_no": "0716542078"
    })
    assert response.status_code == 200
    assert "intern_id" in response.json()
    assert response.json()["intern_id"] == "0001"

def test_get_interns():
    response = client.get("/interns/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_intern_by_id():
    response = client.get("/interns/0001")
    assert response.status_code == 200
    assert response.json()["intern_id"] == "0001"

def test_update_intern():
    response = client.put("/interns/0001", json={
        "name": "Tharindu Updated",
        "address": "198 Updated Rd",
        "email": "updated@example.com",
        "contact_no": "0716542080"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Tharindu Updated"

def test_delete_intern():
    response = client.delete("/interns/0001")
    assert response.status_code == 200
    assert response.json()["message"] == "Intern 0001 deleted successfully."
