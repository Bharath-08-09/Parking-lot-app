from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from app.core.database import get_db
from schemas.parking_tickets import (
    ParkingTicketCreate, ParkingTicketUpdate, ParkingTicketResponse, 
    ParkingTicketList, ParkingTicketExit, ParkingTicketPayment,
    ActiveParkingResponse, PaymentStatus
)
from crud.parking_tickets import parking_ticket_crud

router = APIRouter(prefix="/parking-tickets", tags=["parking-tickets"])

@router.post("/", response_model=ParkingTicketResponse, status_code=status.HTTP_201_CREATED)
def create_parking_ticket(ticket: ParkingTicketCreate, db: Session = Depends(get_db)):
    """Create a new parking ticket (UC1 - Park a Vehicle)."""
    # This will be called by the parking service
    return parking_ticket_crud.create(db, ticket)

@router.get("/", response_model=ParkingTicketList)
def get_parking_tickets(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get parking tickets with pagination."""
    if active_only:
        tickets = parking_ticket_crud.get_active(db, skip=skip, limit=limit)
    else:
        tickets = parking_ticket_crud.get_multi(db, skip=skip, limit=limit)
    
    total = parking_ticket_crud.count(db, active_only=active_only)
    return ParkingTicketList(tickets=tickets, total=total)

@router.get("/recent", response_model=ParkingTicketList)
def get_recent_tickets(minutes: int = Query(30), db: Session = Depends(get_db)):
    """Get tickets for vehicles parked recently (UC15)."""
    cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
    tickets = parking_ticket_crud.get_recent(db, cutoff_time)
    return ParkingTicketList(tickets=tickets, total=len(tickets))

@router.get("/active", response_model=list[ActiveParkingResponse])
def get_active_parking_sessions(db: Session = Depends(get_db)):
    """Get all active parking sessions with details."""
    active_sessions = parking_ticket_crud.get_active_with_details(db)
    return active_sessions

@router.get("/by-lot/{lot_id}", response_model=ParkingTicketList)
def get_tickets_by_lot(lot_id: int, active_only: bool = Query(True), db: Session = Depends(get_db)):
    """Get all tickets for a specific lot (UC17 - for police)."""
    tickets = parking_ticket_crud.get_by_lot(db, lot_id, active_only=active_only)
    return ParkingTicketList(tickets=tickets, total=len(tickets))

@router.get("/{ticket_id}", response_model=ParkingTicketResponse)
def get_parking_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Get parking ticket by ID."""
    ticket = parking_ticket_crud.get(db, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking ticket not found"
        )
    return ticket

@router.get("/number/{ticket_number}", response_model=ParkingTicketResponse)
def get_ticket_by_number(ticket_number: str, db: Session = Depends(get_db)):
    """Get parking ticket by ticket number."""
    ticket = parking_ticket_crud.get_by_ticket_number(db, ticket_number)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    return ticket

@router.patch("/exit", response_model=ParkingTicketResponse)
def exit_parking(ticket_exit: ParkingTicketExit, db: Session = Depends(get_db)):
    """Process vehicle exit (UC2 - Unpark a Vehicle)."""
    # This will be handled by parking service
    ticket = parking_ticket_crud.get_by_ticket_number(db, ticket_exit.ticket_number)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    if not ticket.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket is already processed"
        )
    
    exit_time = ticket_exit.exit_time or datetime.utcnow()
    update_data = {"exit_time": exit_time, "is_active": False}
    
    return parking_ticket_crud.update(db, db_obj=ticket, obj_in=update_data)

@router.patch("/payment", response_model=ParkingTicketResponse)
def process_payment(payment: ParkingTicketPayment, db: Session = Depends(get_db)):
    """Process parking fee payment (UC8)."""
    ticket = parking_ticket_crud.get_by_ticket_number(db, payment.ticket_number)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    update_data = {
        "payment_status": payment.payment_status,
        "parking_fee": payment.parking_fee
    }
    
    return parking_ticket_crud.update(db, db_obj=ticket, obj_in=update_data)

@router.put("/{ticket_id}", response_model=ParkingTicketResponse)
def update_parking_ticket(ticket_id: int, ticket_update: ParkingTicketUpdate, db: Session = Depends(get_db)):
    """Update parking ticket information."""
    ticket = parking_ticket_crud.get(db, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking ticket not found"
        )
    
    return parking_ticket_crud.update(db, db_obj=ticket, obj_in=ticket_update)