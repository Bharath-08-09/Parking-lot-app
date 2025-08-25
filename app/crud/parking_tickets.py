from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from fastapi import HTTPException
from app.models.parking_tickets import ParkingTicket
from app.schemas.parking_tickets import ParkingTicketCreate, ParkingTicketUpdate

def create_parking_ticket(db: Session, payload: ParkingTicketCreate) -> ParkingTicket:
    import uuid
    ticket_number = f"TKT-{uuid.uuid4().hex[:8].upper()}"
    
    obj_data = payload.model_dump()
    obj_data["ticket_number"] = ticket_number
    obj_data["entry_time"] = obj_data.get("entry_time") or datetime.utcnow()
    
    ticket = ParkingTicket(**obj_data)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def get_parking_ticket(db: Session, ticket_id: int) -> ParkingTicket:
    ticket = db.query(ParkingTicket).filter(ParkingTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Parking ticket not found")
    return ticket

def calculate_parking_duration(ticket: ParkingTicket, exit_time: datetime = None) -> int:
    end_time = exit_time or datetime.utcnow()
    duration = end_time - ticket.entry_time
    return int(duration.total_seconds() / 60)

def update_parking_ticket(db: Session, ticket_id: int, payload: ParkingTicketUpdate) -> ParkingTicket:
    ticket = db.query(ParkingTicket).filter(ParkingTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Parking ticket not found")
    
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)
    
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def complete_parking_session(db: Session, ticket_number: str, exit_time: datetime = None) -> ParkingTicket:
    ticket = db.query(ParkingTicket).filter(ParkingTicket.ticket_number == ticket_number).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Parking ticket not found")
    
    ticket.exit_time = exit_time or datetime.utcnow()
    ticket.is_active = False
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def delete_parking_ticket(db: Session, ticket_id: int) -> ParkingTicket:
    ticket = db.query(ParkingTicket).filter(ParkingTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Parking ticket not found")
    
    db.delete(ticket)
    db.commit()
    return ticket