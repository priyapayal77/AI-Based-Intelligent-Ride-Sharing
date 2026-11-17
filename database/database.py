
import sqlite3
from config import DATABASE_PATH


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        str(DATABASE_PATH),
        timeout=30
    )

    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    connection = get_connection()

    try:
        # Create rides first because bookings reference rides.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS rides (
                ride_id TEXT PRIMARY KEY,
                driver_name TEXT,
                pickup_location TEXT,
                drop_location TEXT,
                vehicle_type TEXT,
                seats_available INTEGER NOT NULL DEFAULT 1,
                departure_time TEXT,
                ride_status TEXT DEFAULT 'Available'
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ride_id TEXT NOT NULL,
                passenger_name TEXT NOT NULL,
                pickup_location TEXT NOT NULL,
                drop_location TEXT NOT NULL,
                vehicle_type TEXT NOT NULL,
                fare REAL NOT NULL,
                departure_time TEXT NOT NULL,
                seats_booked INTEGER NOT NULL DEFAULT 1,
                booking_status TEXT NOT NULL DEFAULT 'Confirmed',
                booking_time TEXT NOT NULL,
                FOREIGN KEY (ride_id) REFERENCES rides(ride_id)
            )
        """)
    
        # Create users table for passenger and driver accounts.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                phone_number TEXT NOT NULL UNIQUE,
                email TEXT UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK (
                    role IN ('Passenger', 'Driver')
                ),
                is_phone_verified INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
    
        # ==========================================
        # OTP VERIFICATION TABLE
        # ==========================================

        connection.execute("""
            CREATE TABLE IF NOT EXISTS otp_verifications (
                otp_id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT NOT NULL UNIQUE,
                otp_hash TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                attempts INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()
        print("Database initialized successfully!")

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
def check_rides_schema():
    connection = get_connection()
    try:
        columns = connection.execute(
            "PRAGMA table_info(rides)"
        ).fetchall()

        print("RIDES TABLE COLUMNS:")
        for column in columns:
            print(column["name"])
    finally:
        connection.close()