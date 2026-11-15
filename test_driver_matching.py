
from modules.matching_engine import matching_engine

rides = matching_engine.load_rides()

driver_rides = rides[
    rides["ride_id"].astype(str).str.startswith("DRV")
]

print("Total rides available:", len(rides))
print("\nRegistered driver rides found:", len(driver_rides))

if not driver_rides.empty:
    print("\nDriver rides available for AI matching:")

    print(
        driver_rides[
            [
                "ride_id",
                "city",
                "vehicle_type",
                "seats_available",
                "departure_time"
            ]
        ].to_string(index=False)
    )
else:
    print("No registered driver rides found.")
