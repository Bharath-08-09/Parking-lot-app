from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.schemas.parking_tickets import (
    ParkingTicketCreate, ParkingTicketUpdate, ParkingTicketResponse
)
from app.crud.parking_tickets import (
    create_parking_ticket,
    get_parking_ticket,
    calculate_parking_duration,
    update_parking_ticket,
    complete_parking_session,
    delete_parking_ticket
)

router = APIRouter(prefix="/parking-tickets", tags=["parking-tickets"])

@router.post("/", response_model=ParkingTicketResponse, status_code=status.HTTP_201_CREATED)
def create_new_parking_ticket(ticket: ParkingTicketCreate, db: Session = Depends(get_db)):
    """Create a new parking ticket (UC1 - Park a Vehicle)."""
    return create_parking_ticket(db, ticket)

@router.get("/{ticket_id}", response_model=ParkingTicketResponse)
def get_parking_ticket_by_id(ticket_id: int, db: Session = Depends(get_db)):
    """Get parking ticket by ID."""
    return get_parking_ticket(db, ticket_id)

@router.get("/{ticket_id}/duration")
def get_ticket_duration(ticket_id: int, db: Session = Depends(get_db)):
    """Calculate parking duration for a ticket."""
    ticket = get_parking_ticket(db, ticket_id)
    duration_minutes = calculate_parking_duration(ticket)
    return {
        "ticket_id": ticket_id,
        "duration_minutes": duration_minutes,
        "entry_time": ticket.entry_time,
        "current_time": datetime.utcnow()
    }

@router.put("/{ticket_id}", response_model=ParkingTicketResponse)
def update_parking_ticket_by_id(ticket_id: int, ticket_update: ParkingTicketUpdate, db: Session = Depends(get_db)):
    """Update parking ticket information."""
    return update_parking_ticket(db, ticket_id, ticket_update)

@router.patch("/complete/{ticket_number}", response_model=ParkingTicketResponse)
def complete_parking_session_by_number(ticket_number: str, exit_time: datetime = None, db: Session = Depends(get_db)):
    """Complete a parking session (UC2 - Unpark a Vehicle)."""
    return complete_parking_session(db, ticket_number, exit_time)

@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_parking_ticket_by_id(ticket_id: int, db: Session = Depends(get_db)):
    """Delete parking ticket by ID."""
    delete_parking_ticket(db, ticket_id)