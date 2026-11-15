
import folium


class MapService:

    def create_map(
        self,
        pickup,
        drop,
        route_coordinates=None
    ):

        # Calculate map center dynamically
        center_lat = (
            pickup["latitude"] + drop["latitude"]
        ) / 2

        center_lon = (
            pickup["longitude"] + drop["longitude"]
        ) / 2

        # Create interactive map
        ride_map = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=6,
            tiles="OpenStreetMap"
        )

        # Pickup marker
        folium.Marker(
            location=[
                pickup["latitude"],
                pickup["longitude"]
            ],
            popup=f"Pickup: {pickup['name']}",
            tooltip="Pickup Location",
            icon=folium.Icon(
                color="green",
                icon="play"
            )
        ).add_to(ride_map)

        # Drop marker
        folium.Marker(
            location=[
                drop["latitude"],
                drop["longitude"]
            ],
            popup=f"Drop: {drop['name']}",
            tooltip="Drop Location",
            icon=folium.Icon(
                color="red",
                icon="flag"
            )
        ).add_to(ride_map)

        # Draw road route when coordinates are available
        if route_coordinates:

            folium.PolyLine(
                locations=route_coordinates,
                color="blue",
                weight=5,
                opacity=0.8,
                tooltip="Ride Route"
            ).add_to(ride_map)

        # Automatically fit both locations
        bounds = [
            [
                pickup["latitude"],
                pickup["longitude"]
            ],
            [
                drop["latitude"],
                drop["longitude"]
            ]
        ]

        ride_map.fit_bounds(bounds, padding=(40, 40))

        return ride_map


# Create map service
map_service = MapService()
