
from modules.geocoding import geocoding_service

location = input("Enter a location: ")

results = geocoding_service.search_location(location)

if results:

    print("\nLocation suggestions:\n")

    for index, place in enumerate(results, start=1):

        print(f"{index}. {place['name']}")
        print("Latitude:", place['latitude'])
        print("Longitude:", place['longitude'])
        print("Country:", place['country'])
        print("-" * 50)

else:
    print("No locations found or API unavailable.")
