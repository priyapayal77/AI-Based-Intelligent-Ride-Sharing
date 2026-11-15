
import sqlite3
import pandas as pd

from config import DATABASE_PATH, DATA_DIR


CSV_PATH = DATA_DIR / "rides.csv"


def migrate_database():

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {CSV_PATH}"
        )

    df = pd.read_csv(CSV_PATH)

    required_columns = [
        "ride_id",
        "city",
        "pickup_latitude",
        "pickup_longitude",
        "drop_latitude",
        "drop_longitude",
        "departure_time",
        "vehicle_type",
        "seats_available"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing CSV columns: {missing}"
        )

    connection = sqlite3.connect(str(DATABASE_PATH))

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("BEGIN IMMEDIATE")

        # Add missing columns to existing rides table.
        existing = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(rides)"
            ).fetchall()
        }

        if not existing:
            raise RuntimeError(
                "Rides table not found. Initialize database first."
            )

        new_columns = {
            "city": "TEXT",
            "pickup_latitude": "REAL",
            "pickup_longitude": "REAL",
            "drop_latitude": "REAL",
            "drop_longitude": "REAL",
            "total_seats": "INTEGER DEFAULT 1"
        }

        for column, data_type in new_columns.items():
            if column not in existing:
                connection.execute(
                    f"ALTER TABLE rides ADD COLUMN "
                    f"{column} {data_type}"
                )

        # Import rides without overwriting existing bookings/seats.
        imported = 0

        for _, ride in df.iterrows():

            ride_id = str(ride["ride_id"])

            existing_ride = connection.execute(
                "SELECT ride_id FROM rides WHERE ride_id = ?",
                (ride_id,)
            ).fetchone()

            if existing_ride:
                continue

            seats = int(ride["seats_available"])

            connection.execute("""
                INSERT INTO rides (
                    ride_id,
                    city,
                    pickup_latitude,
                    pickup_longitude,
                    drop_latitude,
                    drop_longitude,
                    departure_time,
                    vehicle_type,
                    total_seats,
                    seats_available,
                    ride_status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Available')
            """, (
                ride_id,
                str(ride["city"]),
                float(ride["pickup_latitude"]),
                float(ride["pickup_longitude"]),
                float(ride["drop_latitude"]),
                float(ride["drop_longitude"]),
                str(ride["departure_time"]),
                str(ride["vehicle_type"]),
                seats,
                seats
            ))

            imported += 1

        connection.commit()

        total = connection.execute(
            "SELECT COUNT(*) FROM rides"
        ).fetchone()[0]

        print("Database migration successful!")
        print(f"New rides imported: {imported}")
        print(f"Total rides in database: {total}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    migrate_database()
