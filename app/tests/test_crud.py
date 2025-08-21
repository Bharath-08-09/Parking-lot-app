def test_create_driver_crud(db):
    from app.crud.drivers import driver_crud
    from app.schemas.drivers import DriverCreate
    new_driver = DriverCreate(name="John Doe", phone="90901", email="john@case.com")
    driver = driver_crud.create(db, new_driver)
    found = driver_crud.get(db, driver.id)
    assert found.email == "john@case.com"

def test_create_parking_lot_crud(db):
    from app.crud.parking_lots import parking_lot_crud
    from app.schemas.parking_lots import ParkingLotCreate
    lot = ParkingLotCreate(name="L1", total_capacity=100, available_slots=100)
    res = parking_lot_crud.create(db, lot)
    assert res.name == "L1"