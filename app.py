
import streamlit as st
import pandas as pd
import time

from datetime import datetime, time as dt_time
from streamlit_folium import st_folium

from modules.geocoding import geocoding_service
from modules.map_service import map_service
from modules.routing import routing_service
from modules.fare_calculator import fare_calculator
from modules.matching_engine import matching_engine

from database.database import initialize_database
from database.booking_database import (
    create_booking,
    get_all_bookings,
    get_passenger_bookings,
    cancel_booking
)
from database.ride_database import (
    create_driver_ride,
    get_driver_rides,
    update_driver_ride_status
)
from database.auth_database import (
    create_user,
    authenticate_user
)
from modules.otp_service import (
    generate_demo_otp,
    verify_demo_otp
)


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="RideMate | AI Ride Sharing",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

initialize_database()


# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "pickup_results": [],
    "drop_results": [],
    "logged_in_user": None,
    "route_data": None,
    "selected_pickup": None,
    "selected_drop": None,
    "departure_datetime": None,
    "matching_results": None,
    "booking_message": None,
    "driver_pickup_results": [],
    "driver_drop_results": [],
    "driver_message": None,
    "driver_name": "",
    "driver_city": "",
    "driver_departure_datetime": None,
    "pending_verification_phone": None,
    "registration_verified": False,
    "registration_message": None,
    "registration_error": None,
    "dashboard_rides": [],
    "auth_mode": "Register",
    "demo_otp_display": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# COSMIC PURPLE + NEON PINK THEME
# =====================================================

st.markdown("""
<style>

/* MAIN BACKGROUND */

.stApp {
    background:
        radial-gradient(
            ellipse at 50% 85%,
            rgba(211,25,160,0.30),
            transparent 38%
        ),
        radial-gradient(
            ellipse at 85% 15%,
            rgba(111,25,200,0.25),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #100523 0%,
            #1B0640 48%,
            #26064A 100%
        );
    color: #FFFFFF;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* NAVBAR */

.rm-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 10px 22px;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    margin-bottom: 25px;
}

.rm-logo {
    font-size: 29px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -1px;
}

.rm-logo span {
    color: #E34BFA;
}

.rm-nav-tag {
    color: #D9C8F5;
    font-size: 14px;
    letter-spacing: 1px;
}

/* HERO */

.rm-hero {
    min-height: 610px;
    padding: 35px 15px 30px;
    position: relative;
    overflow: hidden;
}

.rm-heading {
    font-family: Georgia, serif;
    font-size: clamp(42px, 5vw, 70px);
    font-weight: 800;
    line-height: 1.08;
    color: #FFFFFF;
    margin-top: 25px;
    margin-bottom: 22px;
}

.rm-heading span {
    background: linear-gradient(
        90deg,
        #A855F7,
        #E34BFA,
        #FF79C8
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.rm-description {
    font-size: 19px;
    line-height: 1.6;
    color: #E4D9F5;
    max-width: 570px;
}

/* FEATURES */

.rm-features {
    display: flex;
    gap: 25px;
    margin-top: 35px;
    flex-wrap: wrap;
}

.rm-feature {
    text-align: center;
    min-width: 105px;
    color: #FFFFFF;
    font-size: 14px;
}

.rm-feature-icon {
    font-size: 31px;
    margin-bottom: 8px;
}

/* ROAD SCENE */

.rm-road-scene {
    position: relative;
    height: 230px;
    margin-top: 30px;
    overflow: hidden;
    border-radius: 20px;
    background:
        radial-gradient(
            ellipse at 50% 100%,
            rgba(255,112,194,0.6),
            transparent 50%
        ),
        linear-gradient(
            180deg,
            transparent,
            rgba(115,17,155,0.25)
        );
}

.rm-road {
    position: absolute;
    width: 120%;
    height: 115px;
    left: -10%;
    bottom: -45px;
    border: 8px solid #D946EF;
    border-top: 5px solid #FF9BD9;
    border-radius: 50%;
    transform: rotate(-7deg);
    box-shadow: 0 -5px 25px rgba(229,72,255,0.5);
}

.rm-car {
    position: absolute;
    font-size: 43px;
    filter: drop-shadow(0 0 12px #E34BFA);
    animation: rm-float 4s ease-in-out infinite;
}

.rm-car.one {
    left: 10%;
    bottom: 28px;
}

.rm-car.two {
    left: 53%;
    bottom: 75px;
    font-size: 30px;
    animation-delay: 1s;
}

.rm-car.three {
    right: 12%;
    bottom: 35px;
    font-size: 34px;
    animation-delay: 2s;
}

.rm-location {
    position: absolute;
    right: 32%;
    top: 18px;
    font-size: 30px;
    filter: drop-shadow(0 0 12px #FFB347);
}

@keyframes rm-float {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-8px);
    }
}

/* FORMS */

.rm-card-title {
    font-size: 29px;
    color: #FFFFFF;
    font-weight: 800;
}

.rm-card-subtitle {
    font-size: 14px;
    color: #E2D4F3;
    margin-bottom: 20px;
}

div[data-testid="stForm"] {
    background: rgba(37,12,70,0.82) !important;
    border: 1px solid rgba(222,139,255,0.55) !important;
    border-radius: 22px !important;
    padding: 24px !important;
    box-shadow: 0 0 35px rgba(176,45,255,0.16);
}

/* HEADINGS */

h1, h2, h3, h4 {
    color: #FFFFFF !important;
}

p, label, .stMarkdown {
    color: #E7DDF3;
}

/* INPUT FIELDS */

.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTimeInput input {
    background-color: #321451 !important;
    color: #FFFFFF !important;
    border: 1px solid #80619D !important;
    border-radius: 10px !important;
    min-height: 43px;
}

.stTextInput input::placeholder {
    color: #C9B8DD !important;
}

/* SELECT BOX */

.stSelectbox div[data-baseweb="select"] > div {
    background-color: #321451 !important;
    border: 1px solid #80619D !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
}

/* BUTTONS */

.stButton > button,
.stFormSubmitButton > button,
div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(
        100deg,
        #8B24F5,
        #C026D3,
        #E84BB8
    ) !important;
    color: #FFFFFF !important;
    border: 1px solid #D65AF3 !important;
    border-radius: 11px !important;
    min-height: 45px;
    font-weight: 700 !important;
    box-shadow: 0 0 16px rgba(190,50,245,0.25);
    transition: all 0.25s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 25px rgba(227,75,250,0.55);
}

/* =========================================
   ALL ALERTS: DARK PURPLE + BLACK TEXT
========================================= */

div[data-testid="stAlert"] {
    background: #281044 !important;
    border: 1px solid #A855F7 !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
}

/* Force BLACK text on all alerts */

div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span,
div[data-testid="stAlert"] div,
div[data-testid="stAlert"] [data-testid="stMarkdownContainer"],
div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
    color: #000000 !important;
    opacity: 1 !important;
}

/* SUCCESS */

div[data-testid="stAlert"]:has([data-testid="stSuccessIcon"]) {
    background: #281044 !important;
    border-color: #36C99A !important;
}

/* INFO */

div[data-testid="stAlert"]:has([data-testid="stInfoIcon"]) {
    background: #281044 !important;
    border-color: #719BFF !important;
}

/* WARNING */

div[data-testid="stAlert"]:has([data-testid="stWarningIcon"]) {
    background: #281044 !important;
    border-color: #F0B94A !important;
}

/* ERROR */

div[data-testid="stAlert"]:has([data-testid="stErrorIcon"]) {
    background: #281044 !important;
    border-color: #FF718D !important;
}

/* ALERT ICONS */

div[data-testid="stAlert"] svg {
    color: #000000 !important;
}

/* METRICS AND CARDS */

div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stMetric"] {
    background: rgba(40,14,73,0.85);
    border: 1px solid rgba(204,128,255,0.3);
    border-radius: 16px;
    padding: 15px;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: #16072D;
}

/* TABS */

.stTabs [data-baseweb="tab"] {
    color: #E7DDF3;
}

.stTabs [aria-selected="true"] {
    color: #F06BE6 !important;
}

/* OTHER */

hr {
    border-color: rgba(255,255,255,0.16);
}

a {
    color: #F08AF0 !important;
}

.streamlit-expanderHeader {
    background: #2B104B;
    border-radius: 10px;
}

/* FOOTER */

.rm-footer {
    text-align: center;
    color: #BBA7D4;
    padding: 25px 0;
    border-top: 1px solid rgba(255,255,255,0.12);
    margin-top: 35px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# NAVBAR
# =====================================================

st.html("""
<div class="rm-navbar">
    <div class="rm-logo">🚘 Ride<span>Mate</span></div>
    <div class="rm-nav-tag">
        SMART RIDES &nbsp; | &nbsp; AI MATCHING &nbsp; | &nbsp; SAFE TRAVEL
    </div>
</div>
""")


# =====================================================
# BOOKING MESSAGE
# =====================================================

if st.session_state.booking_message:
    st.success(st.session_state.booking_message)
    st.session_state.booking_message = None


# =====================================================
# REGISTRATION + LOGIN
# =====================================================

if st.session_state.logged_in_user is None:

    left, right = st.columns([1.15, 0.95], gap="large")

    with left:

        st.html("""
        <div class="rm-hero">

            <div class="rm-heading">
                Your Journey,<br>
                <span>Reimagined.</span>
            </div>

            <div class="rm-description">
                AI-powered intelligent ride sharing platform.
                Find, share and book rides with people on your route.
            </div>

            <div class="rm-features">

                <div class="rm-feature">
                    <div class="rm-feature-icon">🚘</div>
                    Smart<br>Ride Matching
                </div>

                <div class="rm-feature">
                    <div class="rm-feature-icon">📍</div>
                    Real-time<br>Route Planning
                </div>

                <div class="rm-feature">
                    <div class="rm-feature-icon">🛡️</div>
                    Safe &<br>Verified Users
                </div>

            </div>

            <div class="rm-road-scene">
                <div class="rm-location">📍</div>
                <div class="rm-car one">🚘</div>
                <div class="rm-car two">🚕</div>
                <div class="rm-car three">🚗</div>
                <div class="rm-road"></div>
            </div>

        </div>
        """)

    with right:

        st.markdown(
            '<div class="rm-card-title">Welcome to RideMate</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="rm-card-subtitle">'
            'Create your account or login to continue.'
            '</div>',
            unsafe_allow_html=True
        )

        auth_choice = st.radio(
            "Choose Account Action",
            ["Register", "Login"],
            horizontal=True,
            key="auth_mode"
        )

        # REGISTRATION

        if auth_choice == "Register":

            st.markdown(
                '<div class="rm-card-title">Create Your Account</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="rm-card-subtitle">'
                'Register as a Passenger or Driver and verify your mobile number.'
                '</div>',
                unsafe_allow_html=True
            )

            with st.form("new_user_registration_form"):

                full_name = st.text_input(
                    "Full Name *",
                    placeholder="Enter your full name"
                )

                phone_number = st.text_input(
                    "Mobile Number *",
                    placeholder="+919876543210"
                )

                role = st.selectbox(
                    "Account Type *",
                    ["Passenger", "Driver"]
                )

                password = st.text_input(
                    "Password *",
                    type="password"
                )

                confirm_password = st.text_input(
                    "Confirm Password *",
                    type="password"
                )

                register_button = st.form_submit_button(
                    "Create Account →",
                    use_container_width=True
                )

            if register_button:

                # Clear old registration messages first
                st.session_state.registration_message = None
                st.session_state.registration_error = None

                if not all([
                    full_name.strip(),
                    phone_number.strip(),
                    password,
                    confirm_password
                ]):

                    st.session_state.registration_error = (
                        "Please fill all required fields."
                    )

                elif password != confirm_password:

                    st.session_state.registration_error = (
                        "Passwords do not match."
                    )

                else:

                    try:

                        user_id = create_user(
                            full_name=full_name.strip(),
                            phone_number=phone_number.strip(),
                            password=password,
                            role=role
                        )

                        st.session_state.pending_verification_phone = (
                            phone_number.strip()
                        )

                        st.session_state.registration_verified = False

                        st.session_state.registration_message = (
                            f"Account created successfully! User ID: {user_id}"
                        )

                    
                except ValueError as error:

    error_message = str(error)

    if "unverified account already exists" in error_message.lower():

        st.session_state.pending_verification_phone = phone_number.strip()
        st.session_state.registration_error = None
        st.session_state.registration_message = (
            "This mobile number is already registered but not verified. "
            "Please complete mobile verification below."
        )

    else:
        st.session_state.registration_error = error_message


        except Exception as error:
        st.session_state.registration_error = (
                            f"Registration failed: {error}"
                        )

            # Show current result only

            if st.session_state.registration_error:
                st.error(st.session_state.registration_error)

            if st.session_state.registration_message:
                st.success(st.session_state.registration_message)
                st.info(
                    "Generate your demo OTP to verify your mobile number."
                )

        # LOGIN

        else:

            st.markdown(
                '<div class="rm-card-title">User Login</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="rm-card-subtitle">'
                'Login to access your RideMate dashboard.'
                '</div>',
                unsafe_allow_html=True
            )

            with st.form("user_login_form"):

                login_phone = st.text_input(
                    "Registered Mobile Number",
                    placeholder="+919876543210"
                )

                login_password = st.text_input(
                    "Password",
                    type="password"
                )

                login_role = st.selectbox(
                    "Login As",
                    ["Passenger", "Driver"]
                )

                login_button = st.form_submit_button(
                    "Login to RideMate →",
                    use_container_width=True
                )

            if login_button:

                if not login_phone.strip() or not login_password:

                    st.error("Please enter mobile number and password.")

                else:

                    try:

                        user = authenticate_user(
                            login_phone.strip(),
                            login_password,
                            login_role
                        )

                        if user is None:

                            st.error(
                                "Invalid mobile number, password or account type."
                            )

                        elif not user["is_phone_verified"]:

                            st.warning(
                                "Please verify your mobile number before login."
                            )

                        else:

                            st.session_state.logged_in_user = user
                            st.rerun()

                    except Exception as error:
                        st.error(f"Login failed: {error}")

    # =====================================================
    # OTP VERIFICATION
    # =====================================================

    if st.session_state.pending_verification_phone:

        st.divider()
        st.subheader("📱 Mobile Number Verification")

        st.write(
            "Registered Mobile Number: "
            + st.session_state.pending_verification_phone
        )

        if st.button(
            "🔐 Generate Demo OTP",
            use_container_width=True
        ):

            try:
                otp = generate_demo_otp(
                    st.session_state.pending_verification_phone
                )

                st.session_state.demo_otp_display = otp
                st.success("Demo OTP generated successfully!")

            except ValueError as error:
                st.warning(str(error))

            except Exception as error:
                st.error(f"OTP generation failed: {error}")

        if st.session_state.demo_otp_display:
            st.info(
                f"🔐 Your Demo OTP is: {st.session_state.demo_otp_display}"
            )
            st.caption("Demo OTP is displayed for testing only.")

        with st.form("demo_otp_verification_form"):

            entered_otp = st.text_input(
                "Enter 6-Digit OTP",
                max_chars=6,
                placeholder="Enter the 6-digit OTP shown above"
            )

            verify_button = st.form_submit_button(
                "✅ Verify Mobile Number",
                use_container_width=True
            )

        if verify_button:

            try:
                verified = verify_demo_otp(
                    st.session_state.pending_verification_phone,
                    entered_otp
                )

                if verified:
                    st.session_state.registration_verified = True
                    st.session_state.pending_verification_phone = None
                    st.session_state.demo_otp_display = None

                    st.success("Mobile number verified successfully!")
                    st.balloons()
                    st.rerun()

            except ValueError as error:
                st.error(str(error))

            except Exception as error:
                st.error(f"Verification failed: {error}")

    if st.session_state.registration_verified:

        st.success(
            "Registration and mobile verification completed! You can now login."
        )

    st.html("""
    <div class="rm-footer">
        🚘 RideMate<br>
        AI-Based Intelligent Ride-Sharing Platform<br>
        Smart Matching • Route Planning • Shared Mobility
    </div>
    """)

    st.stop()


# =====================================================
# LOGGED-IN USER
# =====================================================

logged_in_user = st.session_state.logged_in_user
user_role = logged_in_user["role"]

col1, col2 = st.columns([5, 1])

with col1:

    st.success(f"Welcome back, {logged_in_user['full_name']}!")
    st.caption(f"Logged in as: {user_role}")

with col2:

    if st.button("Logout", key="logout_button"):

        st.session_state.logged_in_user = None
        st.session_state.route_data = None
        st.session_state.matching_results = None

        st.rerun()

st.divider()


# =====================================================
# DRIVER DASHBOARD
# =====================================================

if user_role == "Driver":

    st.title("🚘 Driver Dashboard")
    st.caption(f"Welcome, {logged_in_user['full_name']}!")

    st.header("🚘 Driver Ride Registration")

    with st.form("driver_search_form"):

        driver_name = logged_in_user["full_name"]

        st.text_input(
            "Driver Name",
            value=driver_name,
            disabled=True
        )

        driver_city = st.text_input(
            "City",
            placeholder="Example: Jaipur"
        )

        col1, col2 = st.columns(2)

        with col1:
            driver_pickup_query = st.text_input(
                "Driver Pickup Location",
                placeholder="Enter pickup address"
            )

        with col2:
            driver_drop_query = st.text_input(
                "Driver Drop Location",
                placeholder="Enter destination"
            )

        col3, col4 = st.columns(2)

        with col3:
            driver_date = st.date_input(
                "Departure Date",
                value=datetime.now().date(),
                min_value=datetime.now().date(),
                key="driver_date"
            )

        with col4:
            driver_time = st.time_input(
                "Departure Time",
                value=dt_time(10, 0),
                key="driver_time"
            )

        search_driver_locations = st.form_submit_button(
            "🔍 Search Driver Locations",
            use_container_width=True
        )

    if search_driver_locations:

        if not all([
            driver_name.strip(),
            driver_city.strip(),
            driver_pickup_query.strip(),
            driver_drop_query.strip()
        ]):

            st.error("Please fill all driver and location details.")

        else:

            with st.spinner("Searching driver locations..."):

                try:

                    pickup_results = geocoding_service.search_location(
                        driver_pickup_query,
                        limit=5
                    )

                    time.sleep(1.1)

                    drop_results = geocoding_service.search_location(
                        driver_drop_query,
                        limit=5
                    )

                    st.session_state.driver_pickup_results = (
                        pickup_results or []
                    )

                    st.session_state.driver_drop_results = (
                        drop_results or []
                    )

                    st.session_state.driver_name = driver_name.strip()
                    st.session_state.driver_city = driver_city.strip()

                    st.session_state.driver_departure_datetime = (
                        datetime.combine(driver_date, driver_time)
                    )

                    if not pickup_results:
                        st.error("Driver pickup location not found.")

                    if not drop_results:
                        st.error("Driver drop location not found.")

                    if pickup_results and drop_results:
                        st.success("Driver locations found!")

                except Exception as error:
                    st.error(f"Location search failed: {error}")

    if (
        st.session_state.driver_pickup_results
        and st.session_state.driver_drop_results
    ):

        st.subheader("Confirm Driver Route")

        driver_pickup = st.selectbox(
            "Select Driver Pickup",
            options=st.session_state.driver_pickup_results,
            format_func=lambda item: item["name"],
            key="driver_pickup_selection"
        )

        driver_drop = st.selectbox(
            "Select Driver Drop",
            options=st.session_state.driver_drop_results,
            format_func=lambda item: item["name"],
            key="driver_drop_selection"
        )

        col1, col2 = st.columns(2)

        with col1:
            driver_vehicle = st.selectbox(
                "Vehicle Type",
                ["Bike", "Auto", "Cab"],
                key="driver_vehicle"
            )

        with col2:
            driver_seats = st.number_input(
                "Total Available Seats",
                min_value=1,
                max_value=10,
                value=1,
                step=1,
                key="driver_seats"
            )

        if st.button(
            "✅ Register My Ride",
            use_container_width=True,
            key="register_driver_ride"
        ):

            try:

                if (
                    driver_pickup["latitude"] == driver_drop["latitude"]
                    and driver_pickup["longitude"] == driver_drop["longitude"]
                ):

                    st.error(
                        "Pickup and drop locations cannot be identical."
                    )

                else:

                    ride_id = create_driver_ride(
                        driver_name=st.session_state.driver_name,
                        city=st.session_state.driver_city,
                        pickup_location=driver_pickup["name"],
                        pickup_latitude=driver_pickup["latitude"],
                        pickup_longitude=driver_pickup["longitude"],
                        drop_location=driver_drop["name"],
                        drop_latitude=driver_drop["latitude"],
                        drop_longitude=driver_drop["longitude"],
                        vehicle_type=driver_vehicle,
                        total_seats=driver_seats,
                        departure_time=(
                            st.session_state.driver_departure_datetime
                        )
                    )

                    st.success(
                        f"Ride registered successfully! Ride ID: {ride_id}"
                    )

                    st.session_state.driver_pickup_results = []
                    st.session_state.driver_drop_results = []

            except Exception as error:
                st.error(f"Ride registration failed: {error}")

    # DRIVER RIDE MANAGEMENT

    st.divider()
    st.header("👨‍✈️ Driver Dashboard")

    dashboard_driver_name = logged_in_user["full_name"]

    if st.button(
        "View My Rides",
        use_container_width=True,
        key="view_driver_rides"
    ):

        try:

            st.session_state.dashboard_rides = get_driver_rides(
                dashboard_driver_name
            )

        except Exception as error:
            st.error(f"Could not load driver rides: {error}")

    if st.session_state.dashboard_rides:

        st.success(
            f"{len(st.session_state.dashboard_rides)} registered rides found."
        )

        for ride in st.session_state.dashboard_rides:

            with st.container(border=True):

                st.subheader(f"🚗 Ride: {ride['ride_id']}")

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**City:**", ride["city"])
                    st.write("**Pickup:**", ride["pickup_location"])
                    st.write("**Drop:**", ride["drop_location"])
                    st.write("**Vehicle:**", ride["vehicle_type"])

                with col2:
                    st.write("**Total Seats:**", ride["total_seats"])
                    st.write("**Available Seats:**", ride["seats_available"])
                    st.write("**Departure:**", ride["departure_time"])
                    st.write("**Status:**", ride["ride_status"])

                if ride["ride_status"] in ["Available", "Full"]:

                    col1, col2 = st.columns(2)

                    with col1:

                        if st.button(
                            "✅ Mark Completed",
                            key=f"complete_{ride['ride_id']}"
                        ):

                            try:

                                update_driver_ride_status(
                                    ride_id=ride["ride_id"],
                                    driver_name=dashboard_driver_name,
                                    new_status="Completed"
                                )

                                st.session_state.dashboard_rides = (
                                    get_driver_rides(dashboard_driver_name)
                                )

                                st.rerun()

                            except Exception as error:
                                st.error(str(error))

                    with col2:

                        if st.button(
                            "❌ Cancel Ride",
                            key=f"cancel_ride_{ride['ride_id']}"
                        ):

                            try:

                                update_driver_ride_status(
                                    ride_id=ride["ride_id"],
                                    driver_name=dashboard_driver_name,
                                    new_status="Cancelled"
                                )

                                st.session_state.dashboard_rides = (
                                    get_driver_rides(dashboard_driver_name)
                                )

                                st.rerun()

                            except Exception as error:
                                st.error(str(error))

    else:
        st.info("No rides registered under this driver name.")


# =====================================================
# PASSENGER DASHBOARD
# =====================================================

elif user_role == "Passenger":

    st.title("🚕 Passenger Dashboard")
    st.caption(f"Welcome, {logged_in_user['full_name']}!")

    st.header("📍 Plan Your Journey")

    # LOCATION SEARCH

    with st.form("location_form"):

        col1, col2 = st.columns(2)

        with col1:
            pickup_query = st.text_input(
                "Pickup Location",
                placeholder="Enter pickup city or address"
            )

        with col2:
            drop_query = st.text_input(
                "Drop Location",
                placeholder="Enter destination city or address"
            )

        st.subheader("Departure Details")

        col3, col4 = st.columns(2)

        with col3:
            departure_date = st.date_input(
                "Departure Date",
                value=datetime.now().date()
            )

        with col4:
            departure_time = st.time_input(
                "Departure Time",
                value=dt_time(8, 10)
            )

        search_button = st.form_submit_button(
            "🔍 Search Locations",
            use_container_width=True
        )

    if search_button:

        if not pickup_query.strip() or not drop_query.strip():

            st.error("Please enter both pickup and drop locations.")

        else:

            with st.spinner("Searching worldwide locations..."):

                try:

                    pickup_results = geocoding_service.search_location(
                        pickup_query,
                        limit=5
                    )

                    time.sleep(1.1)

                    drop_results = geocoding_service.search_location(
                        drop_query,
                        limit=5
                    )

                    st.session_state.pickup_results = pickup_results or []
                    st.session_state.drop_results = drop_results or []

                    st.session_state.route_data = None
                    st.session_state.selected_pickup = None
                    st.session_state.selected_drop = None
                    st.session_state.matching_results = None

                    st.session_state.departure_datetime = datetime.combine(
                        departure_date,
                        departure_time
                    )

                    if pickup_results and drop_results:
                        st.success("Locations found successfully!")

                    else:
                        st.warning("One or both locations were not found.")

                except Exception as error:
                    st.error(f"Location search failed: {error}")

    # LOCATION SELECTION

    if (
        st.session_state.pickup_results
        and st.session_state.drop_results
    ):

        st.subheader("Select Your Locations")

        pickup_options = {
            item["name"]: item
            for item in st.session_state.pickup_results
        }

        drop_options = {
            item["name"]: item
            for item in st.session_state.drop_results
        }

        col1, col2 = st.columns(2)

        with col1:
            selected_pickup_name = st.selectbox(
                "Choose Pickup",
                options=list(pickup_options.keys()),
                key="pickup_selection"
            )

        with col2:
            selected_drop_name = st.selectbox(
                "Choose Drop",
                options=list(drop_options.keys()),
                key="drop_selection"
            )

        if st.button(
            "🚕 Find Route & Calculate Fare",
            use_container_width=True
        ):

            pickup = pickup_options[selected_pickup_name]
            drop = drop_options[selected_drop_name]

            if (
                pickup["latitude"] == drop["latitude"]
                and pickup["longitude"] == drop["longitude"]
            ):

                st.error("Pickup and drop locations are identical.")

            else:

                with st.spinner("Calculating road route..."):

                    try:

                        route = routing_service.get_route(
                            pickup,
                            drop
                        )

                        if route:

                            st.session_state.selected_pickup = pickup
                            st.session_state.selected_drop = drop
                            st.session_state.route_data = route
                            st.session_state.matching_results = None

                        else:

                            st.session_state.route_data = None
                            st.error("No driving route available.")

                    except Exception as error:

                        st.session_state.route_data = None
                        st.error(f"Route calculation failed: {error}")

    # ROUTE DETAILS

    if st.session_state.route_data:

        route = st.session_state.route_data

        pickup = st.session_state.selected_pickup
        drop = st.session_state.selected_drop

        st.divider()
        st.header("🗺️ Your Journey")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Road Distance",
            f"{route['distance_km']} KM"
        )

        col2.metric(
            "Estimated Time",
            f"{route['duration_min']:.1f} Minutes"
        )

        col3.metric(
            "Route Status",
            "Available"
        )

        # MAP

        st.subheader("Your Route Map")

        ride_map = map_service.create_map(
            pickup,
            drop,
            route_coordinates=route["coordinates"]
        )

        st_folium(
            ride_map,
            width=None,
            height=500,
            key="ride_map"
        )

        # VEHICLE SELECTION

        st.divider()
        st.header("🚘 Select Your Vehicle")

        vehicle_type = st.selectbox(
            "Choose your preferred vehicle",
            ["Bike", "Auto", "Cab"],
            key="vehicle_selection"
        )

        fare = fare_calculator.calculate_fare(
            distance_km=route["distance_km"],
            duration_min=route["duration_min"],
            vehicle_type=vehicle_type
        )

        st.metric(
            label=f"{vehicle_type} Estimated Fare",
            value=f"₹{fare['total_fare']:.2f}"
        )

        # FARE COMPARISON

        st.subheader("Compare All Vehicles")

        vehicles = ["Bike", "Auto", "Cab"]
        cols = st.columns(3)

        for col, vehicle in zip(cols, vehicles):

            vehicle_fare = fare_calculator.calculate_fare(
                route["distance_km"],
                route["duration_min"],
                vehicle
            )

            with col:
                st.markdown(f"### {vehicle}")

                st.metric(
                    "Estimated Price",
                    f"₹{vehicle_fare['total_fare']:.2f}"
                )

        st.info("Fares are prototype estimates.")

        # AI RIDE MATCHING

        st.divider()
        st.header("🤖 AI-Based Ride Matching")

        st.write(
            "Find passengers travelling along similar routes "
            "at approximately the same time."
        )

        st.write(
            "**Your departure:** "
            + st.session_state.departure_datetime.strftime(
                "%d %b %Y, %I:%M %p"
            )
        )

        find_matches_button = st.button(
            "🔍 Find Shared Rides",
            use_container_width=True
        )

        if find_matches_button:

            with st.spinner("AI is searching for suitable rides..."):

                try:

                    matches = matching_engine.find_best_matches(
                        pickup=pickup,
                        drop=drop,
                        departure_time=st.session_state.departure_datetime
                    )

                    st.session_state.matching_results = matches

                except Exception as error:

                    st.session_state.matching_results = None
                    st.error(f"Matching error: {error}")

        # MATCHING RESULTS AND BOOKING

        if st.session_state.matching_results is not None:

            matches = st.session_state.matching_results

            st.subheader("Recommended Shared Rides")

            if matches:

                st.success(
                    f"{len(matches)} potential matching rides found!"
                )

                for index, match in enumerate(matches[:10], start=1):

                    with st.container(border=True):

                        col1, col2 = st.columns([3, 1])

                        with col1:

                            st.markdown(f"### 🚗 Match #{index}")

                            st.write("**Ride ID:**", match["ride_id"])
                            st.write("**City:**", match["city"])
                            st.write("**Vehicle:**", match["vehicle_type"])

                            st.write(
                                "**Available Seats:**",
                                match["seats_available"]
                            )

                            st.write(
                                "**Departure:**",
                                match["departure_time"]
                            )

                            st.write(
                                "**Pickup Distance:**",
                                f"{match['pickup_distance_km']} KM"
                            )

                            st.write(
                                "**Drop Distance:**",
                                f"{match['drop_distance_km']} KM"
                            )

                            st.write(
                                "**Time Difference:**",
                                f"{match['time_difference_min']} Minutes"
                            )

                            st.write(
                                "**Route Similarity:**",
                                f"{match['route_similarity']}%"
                            )

                        with col2:

                            st.metric(
                                "AI Match Score",
                                f"{match['match_probability']}%"
                            )

                            st.caption(
                                "Model prediction score, "
                                "not a verified success probability."
                            )

                        # BOOK THIS RIDE

                        st.markdown("#### 🎫 Book This Ride")

                        try:

                            available_seats = int(
                                match["seats_available"]
                            )

                            if available_seats < 1:
                                st.warning("No seats available.")
                                continue

                            match_vehicle = match["vehicle_type"]

                            booking_fare = fare_calculator.calculate_fare(
                                distance_km=route["distance_km"],
                                duration_min=route["duration_min"],
                                vehicle_type=match_vehicle
                            )

                            with st.form(
                                f"booking_form_{match['ride_id']}"
                            ):

                                passenger_name = st.text_input(
                                    "Passenger Name",
                                    value=logged_in_user["full_name"],
                                    key=f"passenger_{match['ride_id']}"
                                )

                                seats_booked = st.selectbox(
                                    "Number of Seats",
                                    options=list(
                                        range(1, available_seats + 1)
                                    ),
                                    key=f"seats_{match['ride_id']}"
                                )

                                st.write(
                                    f"**Estimated Fare:** "
                                    f"₹{booking_fare['total_fare']:.2f}"
                                )

                                book_button = st.form_submit_button(
                                    "✅ Book This Ride",
                                    use_container_width=True
                                )

                            if book_button:

                                if not passenger_name.strip():

                                    st.error(
                                        "Please enter your passenger name."
                                    )

                                else:

                                    try:

                                        booking_id = create_booking(
                                            ride_id=match["ride_id"],
                                            passenger_name=passenger_name,
                                            pickup_location=pickup["name"],
                                            drop_location=drop["name"],
                                            vehicle_type=match_vehicle,
                                            fare=booking_fare["total_fare"],
                                            departure_time=match["departure_time"],
                                            seats_booked=seats_booked,
                                            available_seats=available_seats
                                        )

                                        st.session_state.booking_message = (
                                            f"Booking confirmed! "
                                            f"Your Booking ID is {booking_id}."
                                        )

                                        st.rerun()

                                    except ValueError as error:
                                        st.error(str(error))

                                    except Exception as error:
                                        st.error(f"Booking failed: {error}")

                        except Exception as error:
                            st.error(
                                f"Could not prepare booking: {error}"
                            )

            else:

                st.warning(
                    "No suitable shared rides found. "
                    "Try changing your locations or departure time."
                )

        st.caption(
            "Note: Matching recommendations currently use "
            "synthetic demonstration ride records, not live passengers."
        )

    # PASSENGER BOOKING HISTORY

    st.divider()
    st.header("📚 Passenger Booking History")

    passenger_name = logged_in_user["full_name"]

    try:

        bookings = get_passenger_bookings(passenger_name)

        if bookings:

            st.success(f"Found {len(bookings)} booking(s).")

            for booking in bookings:

                with st.container(border=True):

                    col1, col2 = st.columns([3, 1])

                    with col1:

                        st.markdown(
                            f"### 🎫 Booking #{booking['booking_id']}"
                        )

                        st.write("**Passenger:**", booking["passenger_name"])
                        st.write("**Ride ID:**", booking["ride_id"])
                        st.write("**Pickup:**", booking["pickup_location"])
                        st.write("**Drop:**", booking["drop_location"])
                        st.write("**Vehicle:**", booking["vehicle_type"])
                        st.write("**Seats Booked:**", booking["seats_booked"])
                        st.write("**Fare:**", f"₹{booking['fare']:.2f}")
                        st.write("**Departure:**", booking["departure_time"])
                        st.write("**Booking Time:**", booking["booking_time"])

                    with col2:

                        status = booking["booking_status"]

                        if status == "Confirmed":

                            st.success(status)

                            if st.button(
                                "❌ Cancel Booking",
                                key=f"passenger_cancel_{booking['booking_id']}"
                            ):

                                try:

                                    cancelled = cancel_booking(
                                        booking["booking_id"]
                                    )

                                    if cancelled:

                                        st.success(
                                            "Booking cancelled and seats restored."
                                        )

                                        st.rerun()

                                    else:

                                        st.warning(
                                            "Booking could not be cancelled."
                                        )

                                except Exception as error:
                                    st.error(f"Cancellation failed: {error}")

                        else:
                            st.info(status)

        else:
            st.info("No bookings found for this passenger.")

    except Exception as error:
        st.error(f"Could not load booking history: {error}")


# =====================================================
# FOOTER
# =====================================================

st.html("""
<div class="rm-footer">
    🚘 RideMate<br>
    AI-Based Intelligent Ride-Sharing Platform<br>
    Python • Streamlit • OpenStreetMap • Machine Learning
</div>
""")
