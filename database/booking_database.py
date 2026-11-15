
from datetime import datetime
import math

from database.database import get_connection


# ==========================================
# CREATE BOOKING
# ==========================================

def create_booking(
    ride_id,
    passenger_name,
    pickup_location,
    drop_location,
    vehicle_type,
    fare,
    departure_time,
    seats_booked=1,
    available_seats=None
):

    if not passenger_name or not passenger_name.strip():
        raise ValueError("Passenger name is required.")

    try:
        seats_booked = int(seats_booked)
        fare = float(fare)
    except (TypeError, ValueError):
        raise ValueError("Invalid seats or fare value.")

    if seats_booked < 1:
        raise ValueError("At least one seat must be booked.")

    if not math.isfinite(fare) or fare < 0:
        raise ValueError("Invalid fare amount.")

    if not ride_id:
        raise ValueError("Ride ID is required.")

    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        # Verify that the ride already exists.
        ride = connection.execute("""
            SELECT
                ride_id,
                seats_available,
                total_seats,
                ride_status
            FROM rides
            WHERE ride_id = ?
        """, (str(ride_id),)).fetchone()

        if ride is None:
            raise ValueError("Ride not found. Please select a valid ride.")

        if ride["ride_status"] != "Available":
            raise ValueError("This ride is not available for booking.")

        if ride["seats_available"] < seats_booked:
            raise ValueError("Not enough seats available.")

        # Decrease seats and update ride status.
        cursor = connection.execute("""
            UPDATE rides
            SET
                seats_available = seats_available - ?,
                ride_status = CASE
                    WHEN seats_available - ? = 0 THEN 'Full'
                    ELSE 'Available'
                END
            WHERE ride_id = ?
              AND seats_available >= ?
              AND ride_status = 'Available'
        """, (
            seats_booked,
            seats_booked,
            str(ride_id),
            seats_booked
        ))

        if cursor.rowcount != 1:
            raise ValueError("Booking failed. Seats may no longer be available.")

        # Create booking record.
        cursor = connection.execute("""
            INSERT INTO bookings (
                ride_id,
                passenger_name,
                pickup_location,
                drop_location,
                vehicle_type,
                fare,
                departure_time,
                seats_booked,
                booking_status,
                booking_time
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Confirmed', ?)
        """, (
            str(ride_id),
            passenger_name.strip(),
            pickup_location,
            drop_location,
            vehicle_type,
            fare,
            str(departure_time),
            seats_booked,
            datetime.now().isoformat(timespec="seconds")
        ))

        booking_id = cursor.lastrowid

        connection.commit()
        return booking_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ==========================================
# GET ALL BOOKINGS
# ==========================================

def get_all_bookings():

    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT *
            FROM bookings
            ORDER BY booking_id DESC
        """)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


# ==========================================
# GET PASSENGER BOOKINGS
# ==========================================

def get_passenger_bookings(passenger_name):

    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT *
            FROM bookings
            WHERE passenger_name = ?
            ORDER BY booking_id DESC
        """, (passenger_name.strip(),))

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


# ==========================================
# CANCEL BOOKING
# ==========================================

def cancel_booking(booking_id):

    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        booking = connection.execute("""
            SELECT ride_id, seats_booked
            FROM bookings
            WHERE booking_id = ?
              AND booking_status = 'Confirmed'
        """, (int(booking_id),)).fetchone()

        if booking is None:
            connection.rollback()
            return False

        # Cancel the booking.
        connection.execute("""
            UPDATE bookings
            SET booking_status = 'Cancelled'
            WHERE booking_id = ?
              AND booking_status = 'Confirmed'
        """, (int(booking_id),))

        # Restore seats. Reopen a previously full ride.
        connection.execute("""
            UPDATE rides
            SET
                seats_available = MIN(
                    total_seats,
                    seats_available + ?
                ),
                ride_status = CASE
                    WHEN ride_status = 'Full'
                         AND seats_available + ? > 0
                    THEN 'Available'
                    ELSE ride_status
                END
            WHERE ride_id = ?
        """, (
            booking["seats_booked"],
            booking["seats_booked"],
            booking["ride_id"]
        ))

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
