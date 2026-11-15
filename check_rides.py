
from database.database import get_connection

connection = get_connection()

try:
    total = connection.execute(
        "SELECT COUNT(*) FROM rides"
    ).fetchone()[0]

    print("Total rides:", total)

    rows = connection.execute("""
        SELECT
            ride_id,
            city,
            vehicle_type,
            seats_available,
            total_seats,
            departure_time
        FROM rides
        ORDER BY ride_id
        LIMIT 5
    """).fetchall()

    print("\nSample rides:")
    for row in rows:
        print(dict(row))

finally:
    connection.close()
