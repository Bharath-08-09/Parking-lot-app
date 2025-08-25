import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db



@pytest.fixture

# Test Attendants
def test_create_attendant(client):
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "shift_start": "09:00:00",
        "shift_end": "17:00:00"
    }
    response = client.post("/attendants/", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"

def test_get_attendant(client):
    # Create first
    data = {"name": "John", "email": "john@test.com", "phone": "123", "shift_start": "09:00:00", "shift_end": "17:00:00"}
    create_response = client.post("/attendants/", json=data)
    attendant_id = create_response.json()["id"]
    
    # Get
    response = client.get(f"/attendants/{attendant_id}")
    assert response.status_code == 200

# Test Drivers
def test_create_driver(client):
    data = {
        "name": "Jane Driver",
        "phone": "0987654321",
        "license_number": "LIC123456",
        "is_handicapped": False
    }
    response = client.post("/drivers/", json=data)
    assert response.status_code == 201

def test_get_handicap_drivers(client):
    # Create handicap driver
    data = {"name": "Bob", "phone": "111", "license_number": "H123", "is_handicapped": True}
    client.post("/drivers/", json=data)
    
    response = client.get("/drivers/handicap/")
    assert response.status_code == 200
    assert response.json()["total"] == 1

# Test Parking Lots
def test_create_parking_lot(client):
    data = {
        "name": "Main Lot",
        "address": "123 Main St",
        "total_spots": 100,
        "hourly_rate": 5.0
    }
    response = client.post("/parking-lots/", json=data)
    assert response.status_code == 201

# Test Vehicles
def test_create_vehicle(client):
    # Create driver first
    driver_data = {"name": "Driver", "phone": "123", "license_number": "L123", "is_handicapped": False}
    driver_response = client.post("/drivers/", json=driver_data)
    driver_id = driver_response.json()["id"]
    
    # Create vehicle
    vehicle_data = {
        "plate_number": "ABC123",
        "make": "Toyota",
        "model": "Camry",
        "color": "Blue",
        "vehicle_type": "CAR",
        "owner_id": driver_id
    }
    response = client.post("/vehicles/", json=vehicle_data)
    assert response.status_code == 201

def test_search_vehicles(client):
    response = client.get("/vehicles/search?make=Toyota")
    assert response.status_code == 200

# Test Parking Tickets
def test_create_parking_ticket(client):
    # Create dependencies
    attendant_data = {"name": "Att", "email": "att@test.com", "phone": "123", "shift_start": "09:00:00", "shift_end": "17:00:00"}
    attendant = client.post("/attendants/", json=attendant_data).json()
    
    driver_data = {"name": "Driver", "phone": "123", "license_number": "L123", "is_handicapped": False}
    driver = client.post("/drivers/", json=driver_data).json()
    
    lot_data = {"name": "Lot", "address": "123 St", "total_spots": 10, "hourly_rate": 5.0}
    lot = client.post("/parking-lots/", json=lot_data).json()
    
    slot_data = {"lot_id": lot["id"], "slot_number": "A01", "is_available": True, "is_handicap_accessible": False, "is_large": False}
    slot = client.post("/parking-slots/", json=slot_data).json()
    
    vehicle_data = {"plate_number": "XYZ789", "make": "Honda", "model": "Civic", "color": "Red", "vehicle_type": "CAR", "owner_id": driver["id"]}
    vehicle = client.post("/vehicles/", json=vehicle_data).json()