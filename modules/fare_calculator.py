
class FareCalculator:

    # Prototype pricing in INR (Indian Rupees)
    # These are configurable demonstration rates,
    # not official market prices.

    FARE_RATES = {
        "Bike": {
            "base_fare": 20,
            "per_km": 8,
            "per_min": 1,
            "minimum_fare": 30
        },

        "Auto": {
            "base_fare": 25,
            "per_km": 12,
            "per_min": 1.5,
            "minimum_fare": 50
        },

        "Cab": {
            "base_fare": 50,
            "per_km": 18,
            "per_min": 2,
            "minimum_fare": 80
        }
    }

    def calculate_fare(
        self,
        distance_km,
        duration_min,
        vehicle_type
    ):

        if distance_km < 0 or duration_min < 0:
            raise ValueError("Distance and duration cannot be negative.")

        vehicle_type = vehicle_type.strip().title()

        if vehicle_type not in self.FARE_RATES:
            raise ValueError("Invalid vehicle type.")

        rates = self.FARE_RATES[vehicle_type]

        base = rates["base_fare"]

        distance_charge = (
            distance_km * rates["per_km"]
        )

        time_charge = (
            duration_min * rates["per_min"]
        )

        calculated_fare = (
            base + distance_charge + time_charge
        )

        final_fare = max(
            calculated_fare,
            rates["minimum_fare"]
        )

        return {
            "vehicle_type": vehicle_type,
            "base_fare": round(base, 2),
            "distance_charge": round(distance_charge, 2),
            "time_charge": round(time_charge, 2),
            "total_fare": round(final_fare, 2),
            "currency": "INR"
        }


fare_calculator = FareCalculator()
