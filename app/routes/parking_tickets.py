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
from app.utils.standardised_response import standard_response


router = APIRouter(prefix="/parking-tickets", tags=["parking-tickets"])


@router.post("/{ticket_id}")
def create_new_parking_ticket(ticket: ParkingTicketCreate, db: Session = Depends(get_db)):
    ticket_data = create_parking_ticket(db, ticket)
    data = ParkingTicketResponse.model_validate(ticket_data).model_dump()
    return standard_response(201, "Parking ticket created successfully", data)


@router.get("/{ticket_id}")
def get_parking_ticket_by_id(ticket_id: int, db: Session = Depends(get_db)):
    ticket_data = get_parking_ticket(db, ticket_id)
    data = ParkingTicketResponse.model_validate(ticket_data).model_dump()
    return standard_response(200, "Parking ticket fetched successfully", data)


@router.get("/{ticket_id}/duration")
def get_ticket_duration(ticket_id: int, db: Session = Depends(get_db)):
    ticket = get_parking_ticket(db, ticket_id)
    duration_minutes = calculate_parking_duration(ticket)
    data = {
        "ticket_id": ticket_id,
        "duration_minutes": duration_minutes,
        "entry_time": ticket.entry_time,
        "current_time": datetime.utcnow()
    }
    return standard_response(200, "Parking duration calculated successfully", data)


@router.put("/{ticket_id}")
def update_parking_ticket_by_id(ticket_id: int, ticket_update: ParkingTicketUpdate, db: Session = Depends(get_db)):
    ticket_data = update_parking_ticket(db, ticket_id, ticket_update)
    data = ParkingTicketResponse.model_validate(ticket_data).model_dump()
    return standard_response(200, "Parking ticket updated successfully", data)


@router.patch("/complete/{ticket_number}")
def complete_parking_session_by_number(ticket_number: str, exit_time: datetime = None, db: Session = Depends(get_db)):
    ticket_data = complete_parking_session(db, ticket_number, exit_time)
    data = ParkingTicketResponse.model_validate(ticket_data).model_dump()
    return standard_response(200, "Parking session completed successfully", data)


@router.delete("/{ticket_id}")
def delete_parking_ticket_by_id(ticket_id: int, db: Session = Depends(get_db)):
    delete_parking_ticket(db, ticket_id)
    return standard_response(200, "Parking ticket deleted successfully", None)