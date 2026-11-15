
from database.database import initialize_database
from database.booking_database import (
    create_booking,
    get_all_bookings,
    cancel_booking
)


# Step 1: Initialize database

initialize_database()


# Step 2: Create a test booking

booking_id = create_booking(

    ride_id="TEST001",

    passenger_name="Test Passenger",

    pickup_location="Times Square, New York",

    drop_location="Central Park, New York",

    vehicle_type="Cab",

    fare=250,

    departure_time="2026-11-13 08:10",

    seats_booked=1
)


print("\nBooking created successfully!")

print("Booking ID:", booking_id)


# Step 3: Retrieve bookings

bookings = get_all_bookings()

print("\n========== BOOKING HISTORY ==========")

for booking in bookings:

    print("Booking ID:", booking["booking_id"])

    print("Passenger:", booking["passenger_name"])

    print("Ride:", booking["ride_id"])

    print("Fare:", booking["fare"])

    print("Status:", booking["booking_status"])

    print("-" * 40)


# Step 4: Test cancellation

cancelled = cancel_booking(booking_id)

print("\nCancellation test:", cancelled)


# Step 5: Verify final status

bookings = get_all_bookings()

print("\nFinal booking status:")

print(bookings[0]["booking_status"])
