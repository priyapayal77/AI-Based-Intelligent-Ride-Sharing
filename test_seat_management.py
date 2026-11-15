
from database.database import get_connection
from database.booking_database import create_booking, cancel_booking


connection = get_connection()

try:
    ride = connection.execute("""
        SELECT ride_id, seats_available, total_seats,
               departure_time, vehicle_type
        FROM rides
        WHERE ride_id LIKE 'DRV%'
          AND seats_available > 0
          AND ride_status = 'Available'
        ORDER BY rowid DESC
        LIMIT 1
    """).fetchone()

finally:
    connection.close()


if ride is None:
    print("No available driver ride found for testing.")

else:
    ride_id = ride["ride_id"]
    original_seats = ride["seats_available"]

    print("Testing Ride:", ride_id)
    print("Original seats:", original_seats)

    booking_id = None

    try:
        # Book one seat.
        booking_id = create_booking(
            ride_id=ride_id,
            passenger_name="Test Passenger",
            pickup_location="Test Pickup",
            drop_location="Test Drop",
            vehicle_type=ride["vehicle_type"],
            fare=100,
            departure_time=ride["departure_time"],
            seats_booked=1
        )

        print("\nBooking created:", booking_id)

        connection = get_connection()

        try:
            updated = connection.execute("""
                SELECT seats_available, ride_status
                FROM rides
                WHERE ride_id = ?
            """, (ride_id,)).fetchone()

            print("Seats after booking:", updated["seats_available"])
            print("Ride status:", updated["ride_status"])

        finally:
            connection.close()

        # Cancel the booking.
        cancelled = cancel_booking(booking_id)

        print("\nCancellation successful:", cancelled)

        connection = get_connection()

        try:
            restored = connection.execute("""
                SELECT seats_available, ride_status
                FROM rides
                WHERE ride_id = ?
            """, (ride_id,)).fetchone()

            print("Seats after cancellation:", restored["seats_available"])
            print("Final ride status:", restored["ride_status"])

        finally:
            connection.close()

        assert cancelled is True
        assert restored["seats_available"] == original_seats

        print("\nALL SEAT MANAGEMENT TESTS PASSED!")

    except Exception as error:
        print("TEST FAILED:", error)

        if booking_id is not None:
            cancel_booking(booking_id)
