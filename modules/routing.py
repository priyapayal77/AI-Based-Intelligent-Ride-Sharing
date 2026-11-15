
import requests
from config import OSRM_BASE_URL


class RoutingService:

    def __init__(self):
        self.base_url = OSRM_BASE_URL

    def get_route(self, pickup, drop):

        pickup_lat = pickup["latitude"]
        pickup_lon = pickup["longitude"]

        drop_lat = drop["latitude"]
        drop_lon = drop["longitude"]

        # OSRM expects longitude,latitude
        url = (
            f"{self.base_url}/route/v1/driving/"
            f"{pickup_lon},{pickup_lat};"
            f"{drop_lon},{drop_lat}"
        )

        params = {
            "overview": "full",
            "geometries": "geojson",
            "steps": "false"
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            if data.get("code") != "Ok":
                print("Routing error:", data.get("code"))
                return None

            route = data["routes"][0]

            # Convert meters to kilometers
            distance_km = route["distance"] / 1000

            # Convert seconds to minutes
            duration_min = route["duration"] / 60

            # Convert [longitude, latitude]
            # into [latitude, longitude] for Folium
            coordinates = [
                [lat, lon]
                for lon, lat in
                route["geometry"]["coordinates"]
            ]

            return {
                "distance_km": round(distance_km, 2),
                "duration_min": round(duration_min, 2),
                "coordinates": coordinates
            }

        except requests.exceptions.RequestException as error:
            print("Routing API Error:", error)
            return None

        except (KeyError, IndexError, ValueError) as error:
            print("Route data error:", error)
            return None


routing_service = RoutingService()
