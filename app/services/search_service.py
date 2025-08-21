from sqlalchemy.orm import Session
from app.crud.vehicles import vehicle_crud
from app.crud.parking_tickets import parking_ticket_crud
from app.crud.parking_slots import parking_slot_crud

class SearchService:
    def search_by_attributes(self, db: Session, color=None, make=None, vehicle_type=None, lot_id=None):
        results = vehicle_crud.search(db, search_params={
            "color": color,
            "make": make,
            "vehicle_type": vehicle_type
        })  # Adapt schema if needed
        if lot_id:
            tickets = parking_ticket_crud.get_by_lot(db, lot_id, active_only=True)
            vehicle_ids = set(t.vehicle_id for t in tickets)
            results = [v for v in results if v.id in vehicle_ids]
        return results

    def find_recently_parked(self, db: Session, minutes=30):
        from datetime import datetime, timedelta
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        return parking_ticket_crud.get_recent(db, cutoff)

    def cars_in_lot_by_row(self, db: Session, lot_id: int, row_identifier: str):
        slots = parking_slot_crud.get_by_row(db, row_identifier, lot_id=lot_id)
        result = []
        for slot in slots:
            if slot.is_occupied:
                result.append(slot)
        return result

search_service = SearchService()