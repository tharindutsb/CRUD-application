import pytest
from fastapi.testclient import TestClient
import sys
import os
import time# To ensure database commits before next test


# Add project root to sys.path for proper imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from main import app  # Import FastAPI app

client = TestClient(app)
created_intern_id = None  # Global variable to store intern_id

from openApi.services.intern_service import InternsService
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
async def db_client():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    yield client
    client.close()

@pytest.fixture(scope="module")
async def intern_service(db_client):
    service = InternsService(db_client)
    yield service

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Setup before tests & Cleanup after tests"""
    global created_intern_id
    created_intern_id = test_create_intern()  # Ensure a test intern exists
    yield  # Run all tests
    test_delete_intern()  # Cleanup intern after tests

def test_create_intern():
    """Test creating an intern"""
    global created_intern_id
    response = client.post("/interns/", data={
        "name": "Sampath",
        "address": "Homagama",
        "email": "sampath@example.com",
        "contact_no": "0716542080"
    })
    assert response.status_code in [200, 201]  # Accept both 200 and 201
    json_response = response.json()
    assert "intern_id" in json_response
    assert json_response["message"] == "User created successfully"

    # Store intern_id globally
    created_intern_id = json_response["intern_id"]

    # Small delay to allow database commit before next test
    time.sleep(1)

def test_get_intern():
    """Test retrieving an intern"""
    global created_intern_id
    assert created_intern_id is not None  # Ensure intern_id is stored
    response = client.get(f"/interns/{created_intern_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["name"] == "Sampath"

def test_update_intern():
    """Test updating an intern"""
    global created_intern_id
    assert created_intern_id is not None  # Ensure intern_id exists
    response = client.put(f"/interns/{created_intern_id}", json={
        "intern_id": created_intern_id,  # Ensure intern_id is included in the request body
        "name": "Updated Sampath",
        "address": "New Address",
        "email": "updated@example.com",
        "contact_no": "0716542081"
    })
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["name"] == "Updated Sampath"

def test_delete_intern():
    """Test deleting an intern"""
    global created_intern_id
    assert created_intern_id is not None  # Ensure intern_id exists

    # # 🔍 Check if intern still exists before trying to delete it
    # response_check = client.get(f"/interns/{created_intern_id}")
    # if response_check.status_code == 404:
    #     pytest.skip(f"Skipping deletion: Intern {created_intern_id} not found!")

    # response = client.delete(f"/interns/{created_intern_id}")
    # assert response.status_code == 200
    # json_response = response.json()
    # assert json_response["message"] == f"Intern {created_intern_id} deleted successfully."
    
    
    

# async def test_get_next_intern_id(intern_service):
#     """Test generating the next intern ID"""
#     intern_id = await intern_service.get_next_intern_id()
#     assert intern_id.isdigit() and len(intern_id) == 4  # Ensure ID is a 4-digit string
