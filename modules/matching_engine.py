
import pandas as pd
import math

from database.database import get_connection
from machine_learning.predict import predictor


# ==========================================
# MATCHING CONFIGURATION
# ==========================================

MAX_PICKUP_DISTANCE_KM = 3.0
MAX_DROP_DISTANCE_KM = 5.0
MAX_TIME_DIFFERENCE_MIN = 30
MIN_ROUTE_SIMILARITY = 70


# ==========================================
# DISTANCE CALCULATION
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
# BEARING CALCULATION
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


# ==========================================
# ROUTE SIMILARITY
# ==========================================

def calculate_route_similarity(
    pickup1,
    drop1,
    pickup2,
    drop2
):

    bearing1 = calculate_bearing(
        pickup1[0], pickup1[1],
        drop1[0], drop1[1]
    )

    bearing2 = calculate_bearing(
        pickup2[0], pickup2[1],
        drop2[0], drop2[1]
    )

    difference = bearing1 - bearing2

    similarity = (
        (1 + math.cos(difference)) / 2
    ) * 100

    return round(similarity, 2)


# ==========================================
# AI MATCHING ENGINE
# ==========================================

class RideMatchingEngine:

    def __init__(self):
        self.rides = pd.DataFrame()

    # ======================================
    # LOAD RIDES FROM SQLITE DATABASE
    # ======================================

    def load_rides(self):

        connection = get_connection()

        try:
            query = """
                SELECT
                    ride_id,
                    city,
                    pickup_latitude,
                    pickup_longitude,
                    drop_latitude,
                    drop_longitude,
                    departure_time,
                    vehicle_type,
                    seats_available,
                    ride_status
                FROM rides
                WHERE ride_status = 'Available'
                  AND seats_available > 0
                  AND pickup_latitude IS NOT NULL
                  AND pickup_longitude IS NOT NULL
                  AND drop_latitude IS NOT NULL
                  AND drop_longitude IS NOT NULL
            """

            self.rides = pd.read_sql_query(
                query,
                connection
            )

        finally:
            connection.close()

        if self.rides.empty:
            return self.rides

        self.rides["departure_time"] = pd.to_datetime(
            self.rides["departure_time"],
            errors="coerce"
        )

        self.rides["seats_available"] = pd.to_numeric(
            self.rides["seats_available"],
            errors="coerce"
        )

        self.rides = self.rides.dropna(
            subset=[
                "departure_time",
                "pickup_latitude",
                "pickup_longitude",
                "drop_latitude",
                "drop_longitude",
                "seats_available"
            ]
        )

        return self.rides

    # ======================================
    # FIND MATCHING RIDES
    # ======================================

    def find_best_matches(
        self,
        pickup,
        drop,
        departure_time,
        exclude_ride_id=None
    ):

        departure_time = pd.to_datetime(
            departure_time,
            errors="raise"
        )

        # Always fetch the latest database records.
        rides = self.load_rides()

        if rides.empty:
            return []

        matches = []

        pickup_location = (
            float(pickup["latitude"]),
            float(pickup["longitude"])
        )

        drop_location = (
            float(drop["latitude"]),
            float(drop["longitude"])
        )

        for _, ride in rides.iterrows():

            # Do not match a ride with itself.
            if (
                exclude_ride_id is not None
                and str(ride["ride_id"]) == str(exclude_ride_id)
            ):
                continue

            candidate_pickup = (
                float(ride["pickup_latitude"]),
                float(ride["pickup_longitude"])
            )

            candidate_drop = (
                float(ride["drop_latitude"]),
                float(ride["drop_longitude"])
            )

            # Calculate pickup distance.
            pickup_distance = calculate_distance(
                *pickup_location,
                *candidate_pickup
            )

            # Calculate drop distance.
            drop_distance = calculate_distance(
                *drop_location,
                *candidate_drop
            )

            # Calculate time difference.
            time_difference = abs(
                (
                    departure_time
                    - ride["departure_time"]
                ).total_seconds()
            ) / 60

            # Calculate route similarity.
            route_similarity = calculate_route_similarity(
                pickup_location,
                drop_location,
                candidate_pickup,
                candidate_drop
            )

            # Rule-based eligibility filtering.
            if pickup_distance > MAX_PICKUP_DISTANCE_KM:
                continue

            if drop_distance > MAX_DROP_DISTANCE_KM:
                continue

            if time_difference > MAX_TIME_DIFFERENCE_MIN:
                continue

            if route_similarity < MIN_ROUTE_SIMILARITY:
                continue

            # AI model prediction.
            prediction = predictor.predict_match(
                pickup_distance_km=pickup_distance,
                drop_distance_km=drop_distance,
                time_difference_min=time_difference,
                route_similarity=route_similarity
            )

            if prediction["match"] == 1:

                matches.append({

                    "ride_id": str(ride["ride_id"]),

                    "city": ride["city"],

                    "vehicle_type": ride["vehicle_type"],

                    "seats_available": int(
                        ride["seats_available"]
                    ),

                    "pickup_distance_km": round(
                        pickup_distance, 2
                    ),

                    "drop_distance_km": round(
                        drop_distance, 2
                    ),

                    "time_difference_min": round(
                        time_difference, 2
                    ),

                    "route_similarity": route_similarity,

                    "match_probability": prediction[
                        "match_probability"
                    ],

                    "departure_time": str(
                        ride["departure_time"]
                    )

                })

        # Rank by AI match score.
        matches.sort(
            key=lambda item: item["match_probability"],
            reverse=True
        )

        return matches


# ==========================================
# CREATE ENGINE INSTANCE
# ==========================================

matching_engine = RideMatchingEngine()
