
from datetime import datetime, timedelta
from uuid import uuid4

from database.database import get_connection
from database.booking_database import create_booking, cancel_booking
from modules.matching_engine import matching_engine

ride_id = "LAST_" + uuid4().hex[:8].upper()

departure_time = (
    datetime.now() + timedelta(days=1)
).isoformat(timespec="minutes")

connection = get_connection()

try:
    connection.execute("""
        INSERT INTO rides (
            ride_id, driver_name, city,
            pickup_location, pickup_latitude, pickup_longitude,
            drop_location, drop_latitude, drop_longitude,
            vehicle_type, total_seats, seats_available,
            departure_time, ride_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Available')
    """, (
        ride_id, "Last Seat Test", "Jaipur",
        "Pickup", 26.9124, 75.7873,
        "Drop", 26.9200, 75.8000,
        "Cab", 1, 1, departure_time
    ))
    connection.commit()
finally:
    connection.close()

booking_id = None

try:
    booking_id = create_booking(
        ride_id=ride_id,
        passenger_name="Last Seat Passenger",
        pickup_location="Pickup",
        drop_location="Drop",
        vehicle_type="Cab",
        fare=100,
        departure_time=departure_time,
        seats_booked=1
    )

    connection = get_connection()
    try:
        ride = connection.execute("""
            SELECT seats_available, ride_status
            FROM rides WHERE ride_id = ?
        """, (ride_id,)).fetchone()

        print("Seats remaining:", ride["seats_available"])
        print("Ride status:", ride["ride_status"])

        assert ride["seats_available"] == 0
        assert ride["ride_status"] == "Full"

    finally:
        connection.close()

    # Verify full rides are excluded from matching.
    rides = matching_engine.load_rides()

    assert ride_id not in rides["ride_id"].astype(str).values

    print("Full ride excluded from AI matching.")

    # Restore the test ride before cleanup.
    assert cancel_booking(booking_id) is True
    booking_id = None

    print("Last seat booking test passed!")

finally:
    if booking_id is not None:
        cancel_booking(booking_id)

    connection = get_connection()
    try:
        connection.execute(
            "DELETE FROM bookings WHERE ride_id = ?", (ride_id,)
        )
        connection.execute(
            "DELETE FROM rides WHERE ride_id = ?", (ride_id,)
        )
        connection.commit()
    finally:
        connection.close()
