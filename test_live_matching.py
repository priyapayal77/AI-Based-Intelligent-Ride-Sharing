
from modules.matching_engine import matching_engine

# Load a sample ride from the database
rides = matching_engine.load_rides()

if rides.empty:
    print("No rides available.")
else:
    sample = rides.iloc[0]

    pickup = {
        "latitude": float(sample["pickup_latitude"]),
        "longitude": float(sample["pickup_longitude"])
    }

    drop = {
        "latitude": float(sample["drop_latitude"]),
        "longitude": float(sample["drop_longitude"])
    }

    departure_time = sample["departure_time"]

    results = matching_engine.find_best_matches(
        pickup=pickup,
        drop=drop,
        departure_time=departure_time,
        exclude_ride_id=sample["ride_id"]
    )

    print("Test Ride:", sample["ride_id"])
    print("Matching rides found:", len(results))

    for ride in results[:5]:
        print(ride)
