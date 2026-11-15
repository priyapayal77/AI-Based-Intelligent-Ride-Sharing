# 🚘 RideMate – AI-Based Intelligent Ride-Sharing Platform

**Smart Rides | AI Matching | Safe Travel**

RideMate is an AI-powered ride-sharing platform designed to connect passengers and drivers travelling along similar routes. It combines machine learning-based ride matching, real-time route planning, fare estimation, and ride booking to make urban transportation more convenient and efficient.

---

## 📌 Project Overview

RideMate aims to improve the ride-sharing experience by helping passengers discover suitable rides based on pickup location, drop location, departure time, and route similarity.

The platform provides separate dashboards for passengers and drivers, allowing drivers to register available rides and passengers to search, compare, and book suitable rides.

## ✨ Key Features

### 👤 User Authentication
- Passenger and Driver registration.
- Login using registered mobile number and password.
- Password hashing.
- Demo OTP-based mobile number verification.

### 🚗 Driver Dashboard
- Register a ride with pickup and drop locations.
- Select vehicle type: Bike, Auto, or Cab.
- Specify available seats and departure time.
- View and manage registered rides.
- Update ride status.

### 📍 Passenger Dashboard
- Search pickup and drop locations.
- Select locations from geocoding suggestions.
- View road routes on an interactive map.
- Calculate estimated distance and travel time.
- Compare estimated fares for different vehicle types.

### 🤖 AI-Based Ride Matching
- Identify rides travelling along similar routes.
- Compare pickup and drop distances.
- Consider departure-time differences.
- Generate ride match scores using a machine learning model.

### 🎫 Ride Booking
- Book available shared rides.
- Select the number of seats.
- View booking history.
- Cancel bookings.
- Update seat availability after booking or cancellation.

### 🗺️ Route Visualization
- OpenStreetMap-based mapping.
- Interactive Folium maps.
- OSRM-based route information.
- Pickup and drop location markers.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Maps | OpenStreetMap, Folium, Leaflet |
| Geocoding | Geopy, Nominatim |
| Route Calculation | OSRM |
| Database | SQLite |
| Model Storage | Joblib |
| Development Tools | VS Code, Git, GitHub |

---

## 🏗️ Project Structure

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

*Note: The structure above highlights the main project components. Your local repository may contain additional files and tests.*

---

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/priyapayal77/AI-Based-Intelligent-Ride-Sharing.git
```

### 2. Open the project folder

```bash
cd AI-Based-Intelligent-Ride-Sharing
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

---

## 🧠 Machine Learning Approach

RideMate uses a machine learning-based matching approach to identify potentially suitable shared rides.

The matching engine considers features such as:

- Time difference between rides.
- Pickup distance.
- Drop distance.
- Route similarity.
- Detour distance.

The trained model is stored using Joblib and integrated into the ride-matching workflow.

---

## 🎯 Project Objectives

1. Develop an intelligent ride-sharing platform.
2. Improve ride discovery through machine learning-based matching.
3. Provide interactive route visualization.
4. Estimate fares and travel time.
5. Support ride booking and seat management.
6. Encourage efficient utilization of available vehicles.

---

## 🔮 Future Scope

- Real-time GPS tracking.
- Live notifications for passengers and drivers.
- Online payment integration.
- Advanced route optimization.
- Improved ML model evaluation and performance.
- Driver and passenger ratings.
- Deployment as a scalable cloud-based application.

---

## 👩‍💻 Author

**Priya Payal**

B.Tech – Information Technology

GitHub: https://github.com/priyapayal77

---

## 📄 License

This project is developed for academic and educational purposes. A formal open-source license can be added separately if required.
