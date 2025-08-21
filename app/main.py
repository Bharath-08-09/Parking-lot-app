from fastapi import FastAPI, Depends
from app.core.config import settings
from app.core.dependencies import get_current_user
from app.auth.router import router as auth_router

# Import all route modules
from app.routes import (
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


def register_routers(app: FastAPI):
    app.include_router(auth_router)
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
def protected_route(current_user: dict = Depends(get_current_user)):
    """Test endpoint - requires JWT token"""
    return {
        "message": "You are authenticated!", 
        "user_id": current_user["user_id"],
        "user_type": current_user["user_type"]
    }
register_routers(app)