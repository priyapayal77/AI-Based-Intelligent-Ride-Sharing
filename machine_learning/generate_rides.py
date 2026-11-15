
import pandas as pd
import random
import math
from pathlib import Path
from datetime import datetime, timedelta


# ==========================================
# CONFIGURATION
# ==========================================

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_FILE = BASE_DIR / "data" / "rides.csv"

TOTAL_CITIES = 6
RIDES_PER_CITY = 50


# ==========================================
# WORLDWIDE CITY COORDINATES
# ==========================================

CITIES = {
    "Jaipur": (26.9124, 75.7873),
    "New York": (40.7128, -74.0060),
    "Paris": (48.8566, 2.3522),
    "London": (51.5072, -0.1276),
    "Singapore": (1.3521, 103.8198),
    "Sydney": (-33.8688, 151.2093)
}


# Each corridor has a pickup and drop offset
# represented as (east_km, north_km).

CORRIDORS = [
    ((-3, -2), (3, 2)),
    ((-4, 2), (2, -3)),
    ((0, -4), (1, 4)),
    ((-2, 3), (4, 0)),
    ((3, -3), (-3, 3))
]


# ==========================================
# CONVERT DISTANCE OFFSETS TO COORDINATES
# ==========================================

def offset_coordinates(lat, lon, east_km, north_km):

    new_lat = lat + north_km / 111.0

    longitude_factor = (
        111.0 * math.cos(math.radians(lat))
    )

    new_lon = lon + east_km / longitude_factor

    return round(new_lat, 6), round(new_lon, 6)


# ==========================================
# GENERATE RIDE RECORDS
# ==========================================

rides = []

ride_counter = 1

base_date = datetime(2026, 11, 13, 8, 0)

vehicle_types = ["Bike", "Auto", "Cab"]


for city_name, city_center in CITIES.items():

    center_lat, center_lon = city_center

    for corridor_index, corridor in enumerate(CORRIDORS):

        pickup_offset, drop_offset = corridor

        for passenger in range(10):

            # Small location variations
            pickup_east = (
                pickup_offset[0] + random.uniform(-0.2, 0.2)
            )

            pickup_north = (
                pickup_offset[1] + random.uniform(-0.2, 0.2)
            )

            drop_east = (
                drop_offset[0] + random.uniform(-0.3, 0.3)
            )

            drop_north = (
                drop_offset[1] + random.uniform(-0.3, 0.3)
            )

            pickup_lat, pickup_lon = offset_coordinates(
                center_lat,
                center_lon,
                pickup_east,
                pickup_north
            )

            drop_lat, drop_lon = offset_coordinates(
                center_lat,
                center_lon,
                drop_east,
                drop_north
            )

            # Departure time
            departure = (
                base_date
                + timedelta(
                    hours=corridor_index * 2,
                    minutes=random.randint(0, 20)
                )
            )

            # Vehicle type
            vehicle = random.choice(vehicle_types)

            # Available seats
            seats = random.randint(1, 3)

            rides.append({

                "ride_id": f"R{ride_counter:04d}",

                "city": city_name,

                "pickup_latitude": pickup_lat,
                "pickup_longitude": pickup_lon,

                "drop_latitude": drop_lat,
                "drop_longitude": drop_lon,

                "departure_time": departure.strftime(
                    "%Y-%m-%d %H:%M"
                ),

                "vehicle_type": vehicle,

                "seats_available": seats

            })

            ride_counter += 1


# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(rides)


# ==========================================
# VALIDATION
# ==========================================

assert len(df) == 300

assert df.isnull().sum().sum() == 0

assert df["ride_id"].is_unique

assert set(df["vehicle_type"].unique()).issubset(
    set(vehicle_types)
)


# ==========================================
# SAVE DATASET
# ==========================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n================================")
print("300 RIDE DATASET GENERATED")
print("================================")

print("\nTotal rides:", len(df))

print("\nCity-wise ride distribution:")
print(df["city"].value_counts())

print("\nVehicle distribution:")
print(df["vehicle_type"].value_counts())

print("\nFirst five records:")
print(df.head())

print("\nDataset shape:", df.shape)

print("\nMissing values:")
print(df.isnull().sum().sum())

print("\nSaved file:")
print(OUTPUT_FILE)
