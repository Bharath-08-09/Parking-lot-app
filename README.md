# Parking Lot Management System

A backend service built with FastAPI and SQLAlchemy to manage parking lots, slots, drivers, vehicles, and parking transactions. The system provides APIs to register users with different roles, manage parking infrastructure, and handle vehicle parking operations including allocation, release, and transaction history.

## Features

**User Roles:** Admin, Police, Driver, Attendant, Security, Owner

**Parking Management:**
- Create and manage parking lots with capacity tracking
- Define parking slots under each lot (standard, handicap-accessible, large vehicle)
- Real-time lot status monitoring and availability updates

**Driver & Vehicle Management:**
- Register drivers with handicap status support
- Register and link vehicles to drivers
- Support for different vehicle types (Small, Medium, Large, SUV)

**Slot Allocation & Transactions:**
- Smart slot allocation based on vehicle type and driver needs
- Store entry/exit times and calculate parking charges
- Release slot on vehicle exit with payment processing
- Complete parking ticket management system

**Advanced Features:**
- JWT authentication with role-based access control
- Law enforcement search capabilities (by color, make, plate number)
- Recently parked vehicles tracking
- Handicap priority slot assignment
- Large vehicle special slot allocation

## Setup Instructions

**Prerequisites**
- Python 3.8+
- PostgreSQL installed and running

**Installation**

1. Clone the repository
```bash
git clone https://github.com/yourusername/parking-lot-management.git
cd Parking_lot_app
```

2. Create and activate virtual environment
```bash
python -m venv myenv
myenv\Scripts\activate  # Windows
source myenv/bin/activate  # Linux/Mac
```

3. Install dependencies
```bash
pip install -r requirements.txt
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

4. Configure database URL in `app/core/config.py`
```python
DATABASE_URL = "postgresql://username:password@localhost:5432/parking_lot_management"
SECRET_KEY = "your-secret-key-change-in-production"
```

5. Run migrations
```bash
alembic revision --autogenerate -m "Initial tables"
alembic upgrade head
```

6. Start the server
```bash
uvicorn app.main:app --reload
```

## API Endpoints

**Authentication:**
- `/auth/login` - User authentication and JWT token generation
- `/auth/logout` - User logout

**Parking Lots:**
- `/parking-lots/` - Create and manage parking lots
- `/parking-lots/status` - Real-time lot status and capacity
- `/parking-lots/available` - Get available lots only

**Parking Slots:**
- `/parking-slots/` - Manage individual parking slots
- `/parking-slots/handicap` - Get handicap accessible slots
- `/parking-slots/by-row/{row}` - Get slots by row identifier

**Drivers:**
- `/drivers/` - Driver registration and management
- `/drivers/{id}` - Individual driver operations

**Vehicles:**
- `/vehicles/` - Vehicle registration and management
- `/vehicles/search` - Advanced search (color, make, type)
- `/vehicles/plate/{plate}` - Search by plate number

**Parking Operations:**
- `/parking-tickets/` - Park vehicle and create ticket
- `/parking-tickets/exit` - Unpark vehicle and process payment
- `/parking-tickets/recent` - Recently parked vehicles
- `/parking-tickets/by-lot/{lot_id}` - Vehicles in specific lot

**User Roles:**
- `/user-roles/` - Manage user roles and permissions

**Attendants:**
- `/attendants/` - Attendant management

**Notifications:**
- `/lot-notifications/` - Parking lot status notifications

## API Documentation

Access interactive API documentation at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc