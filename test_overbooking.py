
from datetime import datetime, timedelta
from database.database import get_connection
from database.booking_database import create_booking
from uuid import uuid4

ride_id = "TEST_" + uuid4().hex[:8].upper()

departure_time = (
    datetime.now() + timedelta(days=1)
).isoformat(timespec="minutes")

connection = get_connection()

try:
    connection.execute("""
        INSERT INTO rides (
            ride_id,
            driver_name,
            city,
            pickup_location,
            pickup_latitude,
            pickup_longitude,
            drop_location,
            drop_latitude,
            drop_longitude,
            vehicle_type,
            total_seats,
            seats_available,
            departure_time,
            ride_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Available')
    """, (
        ride_id,
        "Overbooking Test Driver",
        "Jaipur",
        "Test Pickup",
        26.9124,
        75.7873,
        "Test Drop",
        26.9200,
        75.8000,
        "Cab",
        1,
        1,
        departure_time
    ))

    connection.commit()

finally:
    connection.close()


print("Test ride created:", ride_id)

try:
    create_booking(
        ride_id=ride_id,
        passenger_name="Test Passenger",
        pickup_location="Test Pickup",
        drop_location="Test Drop",
        vehicle_type="Cab",
        fare=100,
        departure_time=departure_time,
        seats_booked=2
    )

    print("ERROR: Overbooking was incorrectly allowed!")

except ValueError as error:
    print("Booking correctly rejected:", error)


connection = get_connection()

try:
    ride = connection.execute("""
        SELECT seats_available, ride_status
        FROM rides
        WHERE ride_id = ?
    """, (ride_id,)).fetchone()

    booking_count = connection.execute("""
        SELECT COUNT(*)
        FROM bookings
        WHERE ride_id = ?
    """, (ride_id,)).fetchone()[0]

    print("Remaining seats:", ride["seats_available"])
    print("Ride status:", ride["ride_status"])
    print("Bookings created:", booking_count)

    assert ride["seats_available"] == 1
    assert ride["ride_status"] == "Available"
    assert booking_count == 0

    print("\nOVERBOOKING PREVENTION TEST PASSED!")

finally:
    # Remove only this isolated test ride.
    connection.execute(
        "DELETE FROM rides WHERE ride_id = ?",
        (ride_id,)
    )
    connection.commit()
    connection.close()
