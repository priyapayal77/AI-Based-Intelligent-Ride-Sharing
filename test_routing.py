
import time

from modules.geocoding import geocoding_service
from modules.routing import routing_service
from modules.map_service import map_service


# Step 1: Search pickup
pickup_name = input("Enter pickup location: ")

pickup_results = geocoding_service.search_location(
    pickup_name,
    limit=1
)

if not pickup_results:
    print("Pickup location not found.")
    exit()

pickup = pickup_results[0]

# Respect public Nominatim request limit
time.sleep(1.1)

# Step 2: Search drop
drop_name = input("Enter drop location: ")

drop_results = geocoding_service.search_location(
    drop_name,
    limit=1
)

if not drop_results:
    print("Drop location not found.")
    exit()

drop = drop_results[0]

# Step 3: Calculate route
route = routing_service.get_route(pickup, drop)

if not route:
    print("No driving route available.")
    exit()

# Step 4: Display results
print("\n========== ROUTE DETAILS ==========")

print("Pickup:", pickup["name"])
print("Drop:", drop["name"])

print("Distance:", route["distance_km"], "KM")
print("Estimated Time:", route["duration_min"], "Minutes")

# Step 5: Create map with blue route
ride_map = map_service.create_map(
    pickup,
    drop,
    route_coordinates=route["coordinates"]
)

ride_map.save("assets/route_map.html")

print("\nRoute map created successfully!")
print("Open assets/route_map.html in your browser.")
