def test_driver_model(db):
    from app.models.drivers import Driver
    driver = Driver(name="Test", phone="12345", email="a@test.com", is_handicap=True)
    db.add(driver)
    db.commit()
    assert driver.id is not None

def test_vehicle_model(db):
    from app.models.drivers import Driver
    from app.models.vehicles import Vehicle
    driver = Driver(name="Owner", phone="4711", email="b@t.com")
    db.add(driver); db.commit()
    vehicle = Vehicle(plate_number="PLATE123", make="BMW", model="X1", color="Red", vehicle_type="SUV", owner_id=driver.id)
    db.add(vehicle); db.commit()
    assert vehicle.owner_id == driver.id