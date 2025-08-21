from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.core.config import settings
from fastapi import Depends  

# Import all route modules
from routes import (
    auth,
    drivers,
    vehicles,
    attendants,
    parking_lots,
    parking_slots,
    parking_tickets,
    lot_notifications,
    user_roles
)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Parking Lot Management System with JWT Authentication"
)

# Add security scheme for Swagger UI - THIS ENABLES THE AUTHORIZE BUTTON
security = HTTPBearer()

# Include all routers
app.include_router(auth.router)
app.include_router(drivers.router)
app.include_router(vehicles.router)
app.include_router(attendants.router)
app.include_router(parking_lots.router)
app.include_router(parking_slots.router)
app.include_router(parking_tickets.router)
app.include_router(lot_notifications.router)
app.include_router(user_roles.router)

@app.get("/")
def root():
    return {"message": "Parking Lot Management System API"}

# Test endpoint to verify JWT is working
@app.get("/protected")
def protected_route(token = Depends(security)):
    """Test endpoint - requires JWT token via Authorize button"""
    return {"message": "You are authenticated!", "token": token}