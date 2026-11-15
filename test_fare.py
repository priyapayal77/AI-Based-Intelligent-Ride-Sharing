
from modules.fare_calculator import fare_calculator

distance = float(input("Enter distance (KM): "))
duration = float(input("Enter duration (Minutes): "))

print("\nSelect Vehicle:")
print("1. Bike")
print("2. Auto")
print("3. Cab")

choice = input("Enter choice (1-3): ")

vehicles = {
    "1": "Bike",
    "2": "Auto",
    "3": "Cab"
}

if choice not in vehicles:
    print("Invalid vehicle selection.")

else:

    vehicle = vehicles[choice]

    result = fare_calculator.calculate_fare(
        distance,
        duration,
        vehicle
    )

    print("\n========== FARE BREAKDOWN ==========")

    print("Vehicle:", result["vehicle_type"])
    print("Base Fare: Rs.", result["base_fare"])
    print("Distance Charge: Rs.", result["distance_charge"])
    print("Time Charge: Rs.", result["time_charge"])

    print("------------------------------------")

    print("Total Fare: Rs.", result["total_fare"])
    print("Currency:", result["currency"])
