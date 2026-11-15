
import requests
from config import GEOCODING_URL, GEOCODING_USER_AGENT


class GeocodingService:

    def __init__(self):
        self.headers = {
            "User-Agent": GEOCODING_USER_AGENT
        }

    def search_location(self, location_name, limit=5):

        if not location_name or not location_name.strip():
            return []

        params = {
            "q": location_name.strip(),
            "format": "jsonv2",
            "limit": limit,
            "addressdetails": 1
        }

        try:
            response = requests.get(
                GEOCODING_URL,
                params=params,
                headers=self.headers,
                timeout=15
            )

            response.raise_for_status()
            results = response.json()

            locations = []

            for place in results:

                locations.append({
                    "name": place.get("display_name"),
                    "latitude": float(place["lat"]),
                    "longitude": float(place["lon"]),
                    "type": place.get("type"),
                    "country": place.get(
                        "address", {}
                    ).get("country")
                })

            return locations

        except requests.exceptions.RequestException as error:
            print("Geocoding API Error:", error)
            return []

        except (ValueError, KeyError) as error:
            print("Location data error:", error)
            return []


# Create service instance
geocoding_service = GeocodingService()
