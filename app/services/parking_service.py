from sqlalchemy.orm import Session
from app.crud.parking_slots import parking_slot_crud
from app.crud.parking_lots import parking_lot_crud
from app.crud.parking_tickets import parking_ticket_crud
from app.crud.vehicles import vehicle_crud
from app.crud.drivers import driver_crud
from app.schemas.parking_tickets import ParkingTicketCreate
from datetime import datetime
from app.models.parking_slots import ParkingSlot

class ParkingService:
    def park_vehicle(self, db: Session, vehicle_id: int, lot_id: int, driver_id: int, attendant_id: int = None) -> dict:
        # Check if vehicle already parked
        if parking_ticket_crud.get_active_for_vehicle(db, vehicle_id):
            return {"error": "Vehicle already parked."}

        lot = parking_lot_crud.get(db, lot_id)
        if not lot or lot.is_full:
            return {"error": "Parking lot is full."}

        vehicle = vehicle_crud.get(db, vehicle_id)
        driver = driver_crud.get(db, driver_id)

        # Implement your parking strategy here (e.g., use strategy_service)
        slot = self.find_best_slot(db, lot_id, vehicle, driver)
        if slot is None:
            return {"error": "No available slot based on strategy."}

        # Occupy slot, update lot capacity, and create ticket
        parking_slot_crud.occupy_slot(db, slot.id)
        parking_lot_crud.decrease_capacity(db, lot_id)

        ticket_in = ParkingTicketCreate(
            vehicle_id=vehicle_id,
            driver_id=driver_id,
            lot_id=lot_id,
            slot_id=slot.id,
            attendant_id=attendant_id,
            entry_time=datetime.utcnow()
        )
        ticket = parking_ticket_crud.create(db, ticket_in)
        return {"ticket": ticket, "slot": slot}

    def unpark_vehicle(self, db: Session, ticket_number: str, exit_time: datetime = None):
        ticket = parking_ticket_crud.get_by_ticket_number(db, ticket_number)
        if not ticket or not ticket.is_active:
            return {"error": "No active ticket found."}

        parking_slot_crud.free_slot(db, ticket.slot_id)
        parking_lot_crud.increase_capacity(db, ticket.lot_id)
        parking_ticket_crud.complete_parking_session(db, ticket_number, exit_time or datetime.utcnow())
        return {"msg": "Unparked and slot released."}

    def find_best_slot(self, db, lot_id, vehicle, driver):
        from .strategy_service import StrategyService
        strategy = StrategyService()
        return strategy.select_slot(db, lot_id, vehicle, driver)

parking_service = ParkingService()