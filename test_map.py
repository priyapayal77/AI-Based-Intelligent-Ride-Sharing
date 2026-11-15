
from modules.geocoding import geocoding_service
from modules.map_service import map_service

# Get pickup location
pickup_name = input("Enter pickup location: ")

pickup_results = geocoding_service.search_location(
    pickup_name,
    limit=1
)

if not pickup_results:
    print("Pickup location not found.")
    exit()

pickup = pickup_results[0]

# Get drop location
drop_name = input("Enter drop location: ")

drop_results = geocoding_service.search_location(
    drop_name,
    limit=1
)

if not drop_results:
    print("Drop location not found.")
    exit()

drop = drop_results[0]

# Generate map
ride_map = map_service.create_map(
    pickup,
    drop
)

# Save map
ride_map.save("assets/test_map.html")

print("\nMap created successfully!")
print("Open assets/test_map.html in your browser.")
