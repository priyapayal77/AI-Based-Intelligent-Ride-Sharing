
import pandas as pd
import math
from itertools import combinations
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "rides.csv"
OUTPUT_FILE = BASE_DIR / "data" / "matching_pairs.csv"


# ==========================================
# HAVERSINE DISTANCE
# ==========================================

def calculate_distance(lat1, lon1, lat2, lon2):

    earth_radius = 6371

    lat1, lon1, lat2, lon2 = map(
        math.radians,
        [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return earth_radius * c


# ==========================================
# ROUTE DIRECTION
# ==========================================

def calculate_bearing(lat1, lon1, lat2, lon2):

    lat1, lon1, lat2, lon2 = map(
        math.radians,
        [lat1, lon1, lat2, lon2]
    )

    dlon = lon2 - lon1

    y = math.sin(dlon) * math.cos(lat2)

    x = (
        math.cos(lat1) * math.sin(lat2)
        - math.sin(lat1) * math.cos(lat2)
        * math.cos(dlon)
    )

    return math.atan2(y, x)


def calculate_route_similarity(bearing1, bearing2):

    difference = bearing1 - bearing2

    similarity = (
        (1 + math.cos(difference)) / 2
    ) * 100

    return round(similarity, 2)


# ==========================================
# LOAD RAW RIDE DATA
# ==========================================

rides = pd.read_csv(INPUT_FILE)

required_columns = [
    "ride_id",
    "pickup_latitude",
    "pickup_longitude",
    "drop_latitude",
    "drop_longitude",
    "departure_time",
    "vehicle_type",
    "seats_available"
]

missing = set(required_columns) - set(rides.columns)

if missing:
    raise ValueError(
        f"Missing columns: {missing}"
    )

rides["departure_time"] = pd.to_datetime(
    rides["departure_time"],
    errors="coerce"
)

if rides["departure_time"].isna().any():
    raise ValueError("Invalid departure time found.")

if rides[required_columns].isna().any().any():
    raise ValueError("Missing values found in ride data.")


# ==========================================
# GENERATE PASSENGER PAIRS
# ==========================================

matching_data = []

for ride1, ride2 in combinations(
    rides.to_dict("records"), 2
):

    pickup_distance = calculate_distance(
        ride1["pickup_latitude"],
        ride1["pickup_longitude"],
        ride2["pickup_latitude"],
        ride2["pickup_longitude"]
    )

    drop_distance = calculate_distance(
        ride1["drop_latitude"],
        ride1["drop_longitude"],
        ride2["drop_latitude"],
        ride2["drop_longitude"]
    )

    time_difference = abs(
        (
            ride1["departure_time"]
            - ride2["departure_time"]
        ).total_seconds()
    ) / 60

    bearing1 = calculate_bearing(
        ride1["pickup_latitude"],
        ride1["pickup_longitude"],
        ride1["drop_latitude"],
        ride1["drop_longitude"]
    )

    bearing2 = calculate_bearing(
        ride2["pickup_latitude"],
        ride2["pickup_longitude"],
        ride2["drop_latitude"],
        ride2["drop_longitude"]
    )

    route_similarity = calculate_route_similarity(
        bearing1,
        bearing2
    )

    # Initial prototype matching rule
    is_match = (
        pickup_distance <= 3
        and drop_distance <= 5
        and time_difference <= 30
        and route_similarity >= 70
    )

    matching_data.append({

        "ride_id_1": ride1["ride_id"],
        "ride_id_2": ride2["ride_id"],

        "pickup_distance_km": round(
            pickup_distance, 3
        ),

        "drop_distance_km": round(
            drop_distance, 3
        ),

        "time_difference_min": round(
            time_difference, 2
        ),

        "route_similarity": route_similarity,

        "matching_label": int(is_match)
    })


# ==========================================
# SAVE MATCHING DATASET
# ==========================================

matching_df = pd.DataFrame(matching_data)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

matching_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nMatching dataset created successfully!")

print("\nFirst five records:")
print(matching_df.head())

print("\nDataset shape:")
print(matching_df.shape)

print("\nMatching label distribution:")
print(
    matching_df["matching_label"].value_counts()
)

print("\nSaved at:")
print(OUTPUT_FILE)
