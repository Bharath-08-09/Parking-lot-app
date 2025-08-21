from sqlalchemy.orm import Session
from crud.parking_slots import parking_slot_crud

class StrategyService:
    def select_slot(self, db: Session, lot_id: int, vehicle, driver):
        # Handicap driver, prefer closest handicap accessible
        if driver.is_handicap:
            return parking_slot_crud.get_best_slot_for_handicap(db, lot_id)
        # Large cars, prefer large slots
        if vehicle.vehicle_type in ["Large", "SUV"]:
            large_slot = parking_slot_crud.get_large_slots(db, lot_id=lot_id)
            return large_slot[0] if large_slot else None
        # General strategy: pick any standard available
        slots = parking_slot_crud.get_available_by_lot(db, lot_id)
        return slots if slots else None

strategy_service = StrategyService()