
from pathlib import Path

# =====================================
# PROJECT CONFIGURATION
# =====================================

# Main project directory
BASE_DIR = Path(__file__).resolve().parent

# =====================================
# FOLDER PATHS
# =====================================

DATABASE_DIR = BASE_DIR / "database"
DATA_DIR = BASE_DIR / "data"
MODULES_DIR = BASE_DIR / "modules"
ML_DIR = BASE_DIR / "machine_learning"
MODEL_DIR = ML_DIR / "models"
ASSETS_DIR = BASE_DIR / "assets"

# =====================================
# DATABASE CONFIGURATION
# =====================================

DATABASE_PATH = DATABASE_DIR / "rides.db"

# =====================================
# WORLDWIDE MAP CONFIGURATION
# =====================================

# OpenStreetMap
MAP_TILE_URL = "OpenStreetMap"

# Worldwide geocoding using Nominatim
GEOCODING_URL = "https://nominatim.openstreetmap.org/search"

GEOCODING_USER_AGENT = "AI_Ride_Sharing_Project/1.0"

# Worldwide routing using OSRM demo server
OSRM_BASE_URL = "https://router.project-osrm.org"

# =====================================
# MAP SETTINGS
# =====================================

DEFAULT_MAP_ZOOM = 12

PICKUP_MARKER_COLOR = "green"
DROP_MARKER_COLOR = "red"
ROUTE_COLOR = "blue"

# =====================================
# RIDE MATCHING SETTINGS
# =====================================

MAX_TIME_DIFFERENCE_MIN = 30
MAX_PICKUP_DISTANCE_KM = 5

# =====================================
# VEHICLE TYPES
# =====================================

VEHICLE_TYPES = [
    "Bike",
    "Auto",
    "Cab"
]

# =====================================
# APPLICATION SETTINGS
# =====================================

APP_TITLE = "AI-Based Intelligent Ride-Sharing Platform"

APP_ICON = "🚗"

DEBUG = True
