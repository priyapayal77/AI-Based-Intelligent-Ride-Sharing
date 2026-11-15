
from datetime import datetime
from uuid import uuid4

from database.database import get_connection


def create_driver_ride(
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
    departure_time
):
    # Validate driver details
    if not driver_name or not driver_name.strip():
        raise ValueError("Driver name is required.")

    if not city or not city.strip():
        raise ValueError("City is required.")

    if not pickup_location or not drop_location:
        raise ValueError("Pickup and drop locations are required.")

    # Validate coordinates
    coordinates = [
        pickup_latitude,
        pickup_longitude,
        drop_latitude,
        drop_longitude
    ]

    try:
        pickup_latitude, pickup_longitude, drop_latitude, drop_longitude = (
            map(float, coordinates)
        )
    except (TypeError, ValueError):
        raise ValueError("Invalid location coordinates.")

    if not (-90 <= pickup_latitude <= 90):
        raise ValueError("Invalid pickup latitude.")

    if not (-180 <= pickup_longitude <= 180):
        raise ValueError("Invalid pickup longitude.")

    if not (-90 <= drop_latitude <= 90):
        raise ValueError("Invalid drop latitude.")

    if not (-180 <= drop_longitude <= 180):
        raise ValueError("Invalid drop longitude.")

    if (
        pickup_latitude == drop_latitude
        and pickup_longitude == drop_longitude
    ):
        raise ValueError("Pickup and drop locations cannot be identical.")

    if vehicle_type not in ["Bike", "Auto", "Cab"]:
        raise ValueError("Invalid vehicle type.")

    try:
        total_seats = int(total_seats)
    except (TypeError, ValueError):
        raise ValueError("Invalid number of seats.")

    if total_seats < 1 or total_seats > 10:
        raise ValueError("Seats must be between 1 and 10.")

    try:
        departure = datetime.fromisoformat(str(departure_time))
    except ValueError:
        raise ValueError("Invalid departure date or time.")

    if departure <= datetime.now():
        raise ValueError("Departure must be in the future.")

    ride_id = "DRV" + uuid4().hex[:10].upper()

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
            driver_name.strip(),
            city.strip(),
            pickup_location,
            pickup_latitude,
            pickup_longitude,
            drop_location,
            drop_latitude,
            drop_longitude,
            vehicle_type,
            total_seats,
            total_seats,
            departure.isoformat(timespec="minutes")
        ))

        connection.commit()
        return ride_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

# ==========================================
# DRIVER RIDE STATUS MANAGEMENT
# ==========================================

def update_driver_ride_status(ride_id, driver_name, new_status):

    allowed_statuses = ["Completed", "Cancelled"]

    if new_status not in allowed_statuses:
        raise ValueError("Invalid ride status.")

    if not driver_name or not driver_name.strip():
        raise ValueError("Driver name is required.")

    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        ride = connection.execute("""
            SELECT ride_id, ride_status
            FROM rides
            WHERE ride_id = ?
              AND driver_name = ?
        """, (str(ride_id), driver_name.strip())).fetchone()

        if ride is None:
            raise ValueError("Ride not found for this driver.")

        if ride["ride_status"] not in ["Available", "Full"]:
            raise ValueError(
                f"Cannot update ride with status: {ride['ride_status']}"
            )

        connection.execute("""
            UPDATE rides
            SET ride_status = ?
            WHERE ride_id = ?
              AND driver_name = ?
        """, (
            new_status,
            str(ride_id),
            driver_name.strip()
        ))

        # If driver cancels a ride, cancel its confirmed bookings too.
        if new_status == "Cancelled":
            connection.execute("""
                UPDATE bookings
                SET booking_status = 'Cancelled'
                WHERE ride_id = ?
                  AND booking_status = 'Confirmed'
            """, (str(ride_id),))

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ==========================================
# GET DRIVER RIDES
# ==========================================

def get_driver_rides(driver_name):

    if not driver_name or not driver_name.strip():
        return []

    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT
                ride_id,
                driver_name,
                city,
                pickup_location,
                drop_location,
                vehicle_type,
                total_seats,
                seats_available,
                departure_time,
                ride_status
            FROM rides
            WHERE driver_name = ?
            ORDER BY rowid DESC
        """, (driver_name.strip(),)).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()
