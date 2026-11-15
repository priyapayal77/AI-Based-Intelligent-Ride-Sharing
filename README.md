# 🚘 RideMate – AI-Based Intelligent Ride-Sharing Platform

### Your Journey, Reimagined.

**RideMate** is an AI-powered intelligent ride-sharing platform designed to connect passengers and drivers travelling along similar routes. The platform uses machine learning-based ride matching, interactive maps, route planning, fare estimation, and ride booking to provide a smarter and more convenient transportation experience.

---

## 🌟 Project Overview

Traditional transportation services often involve individual rides, higher travel costs, and inefficient vehicle utilization.

RideMate aims to address these challenges by enabling passengers to find and share rides with drivers travelling in similar directions.

The platform provides separate dashboards for passengers and drivers, allowing users to register, search for rides, manage bookings, and view route information.

## ✨ Key Features

### 👤 1. User Authentication
- Passenger and Driver registration.
- Secure login using mobile number and password.
- Password hashing.
- Demo OTP-based mobile number verification.

### 🚗 2. Driver Dashboard
- Register new rides.
- Enter pickup and drop locations.
- Select vehicle type: Bike, Auto, or Cab.
- Specify available seats and departure time.
- View registered rides.
- Manage ride status.

### 📍 3. Passenger Dashboard
- Search pickup and drop locations.
- Location suggestions through geocoding.
- Interactive route visualization.
- Road distance and estimated travel time.
- Fare calculation and vehicle comparison.

### 🤖 4. AI-Based Ride Matching
- Identify rides travelling along similar routes.
- Compare pickup and drop distances.
- Consider departure-time differences.
- Evaluate route similarity.
- Generate ride match scores using a machine learning model.

### 🎫 5. Ride Booking Management
- Book available shared rides.
- Select the number of seats.
- View booking history.
- Cancel bookings.
- Update available seats after booking and cancellation.

### 🗺️ 6. Interactive Route Planning
- OpenStreetMap integration.
- Folium-based interactive maps.
- OSRM-based road route calculation.
- Pickup and drop location markers.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Mapping | OpenStreetMap, Folium, Leaflet |
| Geocoding | Geopy, Nominatim |
| Route Calculation | OSRM API |
| Database | SQLite |
| Model Serialization | Joblib |
| Development Tools | VS Code, Git, GitHub |

---

## 🧠 Machine Learning Approach

RideMate incorporates a machine learning-based ride-matching system to identify potentially suitable rides.

The matching process considers the following features:

- `time_difference_min`
- `pickup_distance_km`
- `drop_distance_km`
- `route_similarity`
- `detour_distance_km`

A trained machine learning model is integrated into the matching workflow to generate ride match scores.

The model and its feature configuration are stored using Joblib.

---

## 📂 Project Structure

```text
AI-Ride-Sharing/
│
├── app.py
│
├── database/
│   ├── database.py
│   ├── auth_database.py
│   ├── ride_database.py
│   └── booking_database.py
│
├── machine_learning/
│   ├── models/
│   │   ├── ride_match_model.pkl
│   │   └── feature_names.pkl
│   ├── generate_rides.py
│   ├── predict.py
│   ├── prepare_dataset.py
│   └── train_model.py
│
├── modules/
│   ├── fare_calculator.py
│   ├── geocoding.py
│   ├── map_service.py
│   ├── matching_engine.py
│   ├── otp_service.py
│   └── routing.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

*Note: This is a simplified view of the main project structure. Additional testing and configuration files may also be present.*

---

## ⚙️ Installation and Setup

Follow these steps to run RideMate locally.

### Step 1: Clone the Repository

```bash
git clone https://github.com/priyapayal77/AI-Based-Intelligent-Ride-Sharing.git
```

### Step 2: Navigate to the Project Directory

```bash
cd AI-Based-Intelligent-Ride-Sharing
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will normally be available at:

**http://localhost:8501**

---

## 🎯 Project Objectives

1. Develop an intelligent ride-sharing platform.
2. Implement machine learning-based ride matching.
3. Reduce unnecessary individual vehicle journeys through ride sharing.
4. Provide interactive route planning and visualization.
5. Calculate estimated fares and travel times.
6. Implement ride booking and seat management.

---

## 🔮 Future Scope

- Real-time GPS tracking.
- Live driver and passenger notifications.
- Online payment integration.
- Advanced route optimization.
- Improved machine learning model evaluation.
- Driver and passenger rating systems.
- Cloud deployment and scalability.

---

## 👩‍💻 Author

**Priya Payal**

B.Tech – Information Technology

GitHub: [priyapayal77](https://github.com/priyapayal77)

Project Repository: [AI-Based Intelligent Ride-Sharing Platform](https://github.com/priyapayal77/AI-Based-Intelligent-Ride-Sharing)

---

## 📄 License

This project is developed for academic and educational purposes. A suitable open-source license can be added separately if the project is intended for public reuse.
