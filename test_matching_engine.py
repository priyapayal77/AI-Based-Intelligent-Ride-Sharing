
from modules.matching_engine import matching_engine

rides = matching_engine.load_rides()

print("Total database rides available for matching:", len(rides))

print("\nFirst 5 rides:")
print(
    rides[
        [
            "ride_id",
            "city",
            "vehicle_type",
            "seats_available"
        ]
    ].head()
)
