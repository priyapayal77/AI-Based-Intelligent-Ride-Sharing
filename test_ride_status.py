
from database.ride_database import (
    update_driver_ride_status,
    get_driver_rides
)

driver_name = "surendra"

rides = get_driver_rides(driver_name)

print("Driver rides found:", len(rides))

for ride in rides:
    print(ride)

if rides:
    ride = rides[0]

    if ride["ride_status"] in ["Available", "Full"]:

        result = update_driver_ride_status(
            ride_id=ride["ride_id"],
            driver_name=driver_name,
            new_status="Completed"
        )

        print("\nStatus update successful:", result)

        updated_rides = get_driver_rides(driver_name)

        updated_ride = next(
            item for item in updated_rides
            if item["ride_id"] == ride["ride_id"]
        )

        print("Updated status:", updated_ride["ride_status"])

        assert updated_ride["ride_status"] == "Completed"

        print("\nRIDE STATUS TEST PASSED!")

    else:
        print("Selected ride is already completed or cancelled.")

else:
    print("No rides found for this driver.")
