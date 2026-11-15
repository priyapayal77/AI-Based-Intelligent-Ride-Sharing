
from database.database import get_connection

connection = get_connection()

try:
    rides = connection.execute("""
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
        WHERE ride_id LIKE 'DRV%'
        ORDER BY rowid DESC
        LIMIT 5
    """).fetchall()

    if rides:
        print("Registered Driver Rides:\n")

        for ride in rides:
            print(dict(ride))
    else:
        print("No driver rides found.")

finally:
    connection.close()
