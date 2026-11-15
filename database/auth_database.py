
import hashlib
import hmac
import re
import secrets

from database.database import get_connection


# ==========================================
# PASSWORD HASHING
# ==========================================

def hash_password(password):

    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        310000
    ).hex()

    return f"pbkdf2_sha256${salt}${password_hash}"


# ==========================================
# PASSWORD VERIFICATION
# ==========================================

def verify_password(password, stored_hash):

    try:
        algorithm, salt, original_hash = stored_hash.split("$")

        if algorithm != "pbkdf2_sha256":
            return False

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            310000
        ).hex()

        return hmac.compare_digest(
            new_hash,
            original_hash
        )

    except (ValueError, AttributeError):
        return False


# ==========================================
# USER REGISTRATION
# ==========================================

def create_user(full_name, phone_number, password, role):

    full_name = full_name.strip()
    phone_number = phone_number.strip()

    if not full_name:
        raise ValueError("Full name is required.")

    if not re.fullmatch(r"\+[1-9]\d{7,14}", phone_number):
        raise ValueError(
            "Enter mobile number with country code. "
            "Example: +919876543210"
        )

    if len(password) < 8:
        raise ValueError(
            "Password must contain at least 8 characters."
        )

    if role not in ["Passenger", "Driver"]:
        raise ValueError("Invalid account role.")

    password_hash = hash_password(password)

    connection = get_connection()

    try:

        cursor = connection.execute(
            """
            INSERT INTO users (
                full_name,
                phone_number,
                password_hash,
                role
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                full_name,
                phone_number,
                password_hash,
                role
            )
        )

        connection.commit()

        return cursor.lastrowid

    except Exception as error:

        connection.rollback()

        if "UNIQUE constraint failed" in str(error):
            raise ValueError(
                "This mobile number is already registered."
            )

        raise

    finally:
        connection.close()


# ==========================================
# GET USER BY PHONE NUMBER
# ==========================================

def get_user_by_phone(phone_number):

    connection = get_connection()

    try:

        user = connection.execute(
            """
            SELECT
                user_id,
                full_name,
                phone_number,
                role,
                is_phone_verified,
                created_at
            FROM users
            WHERE phone_number = ?
            """,
            (phone_number.strip(),)
        ).fetchone()

        return dict(user) if user else None

    finally:
        connection.close()


# ==========================================
# MARK MOBILE NUMBER AS VERIFIED
# ==========================================

def mark_phone_verified(phone_number):

    connection = get_connection()

    try:

        cursor = connection.execute(
            """
            UPDATE users
            SET is_phone_verified = 1
            WHERE phone_number = ?
            """,
            (phone_number.strip(),)
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


# ==========================================
# USER LOGIN
# ==========================================

def authenticate_user(phone_number, password, role):

    connection = get_connection()

    try:

        user = connection.execute(
            """
            SELECT *
            FROM users
            WHERE phone_number = ?
            AND role = ?
            """,
            (phone_number.strip(), role)
        ).fetchone()

        if not user:
            return None

        if not verify_password(
            password,
            user["password_hash"]
        ):
            return None

        # OTP verification is required before login.
        if not user["is_phone_verified"]:
            return None

        return {
            "user_id": user["user_id"],
            "full_name": user["full_name"],
            "phone_number": user["phone_number"],
            "role": user["role"],
            "is_phone_verified": user["is_phone_verified"]
        }

    finally:
        connection.close()
