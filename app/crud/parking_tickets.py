from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from app.models.parking_tickets import ParkingTicket
from app.schemas.parking_tickets import ParkingTicketCreate, ParkingTicketUpdate, ActiveParkingResponse

class ParkingTicketCRUD:
    def create(self, db: Session, obj_in: ParkingTicketCreate) -> ParkingTicket:
        """Create a new parking ticket."""
        # Generate ticket number (simple implementation)
        import uuid
        ticket_number = f"TKT-{uuid.uuid4().hex[:8].upper()}"
        
        db_obj = ParkingTicket(
            ticket_number=ticket_number,
            vehicle_id=obj_in.vehicle_id,
            driver_id=obj_in.driver_id,
            lot_id=obj_in.lot_id,
            slot_id=obj_in.slot_id,
            attendant_id=obj_in.attendant_id,
            entry_time=obj_in.entry_time or datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[ParkingTicket]:
        """Get parking ticket by ID."""
        return db.query(ParkingTicket).filter(ParkingTicket.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ParkingTicket]:
        """Get multiple parking tickets with pagination."""
        return db.query(ParkingTicket).offset(skip).limit(limit).all()

    def get_by_ticket_number(self, db: Session, ticket_number: str) -> Optional[ParkingTicket]:
        """Get ticket by ticket number."""
        return db.query(ParkingTicket).filter(ParkingTicket.ticket_number == ticket_number).first()

    def get_active(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ParkingTicket]:
        """Get active parking tickets."""
        return db.query(ParkingTicket).filter(
            ParkingTicket.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_vehicle(self, db: Session, vehicle_id: int, active_only: bool = True) -> List[ParkingTicket]:
        """Get tickets for a specific vehicle."""
        query = db.query(ParkingTicket).filter(ParkingTicket.vehicle_id == vehicle_id)
        if active_only:
            query = query.filter(ParkingTicket.is_active == True)
        return query.all()

    def get_by_driver(self, db: Session, driver_id: int, active_only: bool = True) -> List[ParkingTicket]:
        """Get tickets for a specific driver."""
        query = db.query(ParkingTicket).filter(ParkingTicket.driver_id == driver_id)
        if active_only:
            query = query.filter(ParkingTicket.is_active == True)
        return query.all()

    def get_by_lot(self, db: Session, lot_id: int, active_only: bool = True) -> List[ParkingTicket]:
        """Get all tickets for a specific lot (UC17)."""
        query = db.query(ParkingTicket).filter(ParkingTicket.lot_id == lot_id)
        if active_only:
            query = query.filter(ParkingTicket.is_active == True)
        return query.all()

    def get_recent(self, db: Session, cutoff_time: datetime) -> List[ParkingTicket]:
        """Get tickets for vehicles parked recently (UC15)."""
        return db.query(ParkingTicket).filter(
            ParkingTicket.entry_time >= cutoff_time,
            ParkingTicket.is_active == True
        ).all()

    def get_active_with_details(self, db: Session) -> List[ActiveParkingResponse]:
        """Get active parking sessions with full details."""
        tickets = db.query(ParkingTicket).options(
            joinedload(ParkingTicket.vehicle),
            joinedload(ParkingTicket.driver),
            joinedload(ParkingTicket.lot),
            joinedload(ParkingTicket.slot)
        ).filter(ParkingTicket.is_active == True).all()
        
        result = []
        for ticket in tickets:
            duration_minutes = int((datetime.utcnow() - ticket.entry_time).total_seconds() / 60)
            result.append(ActiveParkingResponse(
                id=ticket.id,
                ticket_number=ticket.ticket_number,
                vehicle_plate=ticket.vehicle.plate_number,
                driver_name=ticket.driver.name,
                lot_name=ticket.lot.name,
                slot_number=ticket.slot.slot_number,
                entry_time=ticket.entry_time,
                duration_minutes=duration_minutes
            ))
        return result

    def get_active_for_vehicle(self, db: Session, vehicle_id: int) -> Optional[ParkingTicket]:
        """Get active ticket for a vehicle (to check if already parked)."""
        return db.query(ParkingTicket).filter(
            ParkingTicket.vehicle_id == vehicle_id,
            ParkingTicket.is_active == True
        ).first()

    def calculate_parking_duration(self, ticket: ParkingTicket, exit_time: datetime = None) -> int:
        """Calculate parking duration in minutes."""
        end_time = exit_time or datetime.utcnow()
        duration = end_time - ticket.entry_time
        return int(duration.total_seconds() / 60)

    def update(self, db: Session, *, db_obj: ParkingTicket, obj_in: ParkingTicketUpdate) -> ParkingTicket:
        """Update parking ticket information."""
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def complete_parking_session(self, db: Session, ticket_number: str, exit_time: datetime = None) -> ParkingTicket:
        """Complete a parking session (UC2)."""
        ticket = self.get_by_ticket_number(db, ticket_number)
        if ticket:
            ticket.exit_time = exit_time or datetime.utcnow()
            ticket.is_active = False
            db.add(ticket)
            db.commit()
            db.refresh(ticket)
        return ticket

    def remove(self, db: Session, *, id: int) -> ParkingTicket:
        """Delete parking ticket by ID."""
        obj = db.query(ParkingTicket).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def count(self, db: Session, active_only: bool = False) -> int:
        """Count total parking tickets."""
        if active_only:
            return db.query(ParkingTicket).filter(ParkingTicket.is_active == True).count()
        return db.query(ParkingTicket).count()

parking_ticket_crud = ParkingTicketCRUD()