
import hashlib
import hmac
import secrets

from datetime import datetime, timedelta

from database.database import get_connection
from database.auth_database import (
    get_user_by_phone,
    mark_phone_verified
)


# ==========================================
# OTP CONFIGURATION
# ==========================================

OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 5
MAX_ATTEMPTS = 5
RESEND_COOLDOWN_SECONDS = 30


# ==========================================
# OTP HASHING
# ==========================================

def hash_otp(otp):
    return hashlib.sha256(
        otp.encode("utf-8")
    ).hexdigest()


# ==========================================
# GENERATE DEMO OTP
# ==========================================

def generate_demo_otp(phone_number):

    phone_number = phone_number.strip()

    if not phone_number:
        raise ValueError("Phone number is required.")

    user = get_user_by_phone(phone_number)

    if not user:
        raise ValueError("No registered account found.")

    if user["is_phone_verified"]:
        raise ValueError("Mobile number is already verified.")

    connection = get_connection()

    try:
        existing = connection.execute(
            """
            SELECT created_at
            FROM otp_verifications
            WHERE phone_number = ?
            """,
            (phone_number,)
        ).fetchone()

        if existing:
            created_at = datetime.fromisoformat(
                existing["created_at"]
            )

            elapsed = (
                datetime.now() - created_at
            ).total_seconds()

            if elapsed < RESEND_COOLDOWN_SECONDS:
                remaining = int(
                    RESEND_COOLDOWN_SECONDS - elapsed
                ) + 1

                raise ValueError(
                    f"Please wait {remaining} seconds "
                    "before requesting another OTP."
                )

        # Generate a random 6-digit OTP
        otp = str(
            secrets.randbelow(10 ** OTP_LENGTH)
        ).zfill(OTP_LENGTH)

        otp_hash = hash_otp(otp)

        expires_at = (
            datetime.now() +
            timedelta(minutes=OTP_EXPIRY_MINUTES)
        ).isoformat()

        connection.execute(
            """
            INSERT INTO otp_verifications (
                phone_number,
                otp_hash,
                expires_at,
                attempts,
                created_at
            )
            VALUES (?, ?, ?, 0, ?)

            ON CONFLICT(phone_number)
            DO UPDATE SET
                otp_hash = excluded.otp_hash,
                expires_at = excluded.expires_at,
                attempts = 0,
                created_at = excluded.created_at
            """,
            (
                phone_number,
                otp_hash,
                expires_at,
                datetime.now().isoformat()
            )
        )

        connection.commit()

        # Return OTP to app.py for demo display.
        # Never display OTP this way in production.
        return otp

    finally:
        connection.close()


# ==========================================
# VERIFY DEMO OTP
# ==========================================

def verify_demo_otp(phone_number, entered_otp):

    phone_number = phone_number.strip()
    entered_otp = entered_otp.strip()

    if (
        not entered_otp.isdigit()
        or len(entered_otp) != OTP_LENGTH
    ):
        raise ValueError(
            "Enter a valid 6-digit OTP."
        )

    connection = get_connection()

    try:
        record = connection.execute(
            """
            SELECT *
            FROM otp_verifications
            WHERE phone_number = ?
            """,
            (phone_number,)
        ).fetchone()

        if not record:
            raise ValueError(
                "OTP not found. Request a new OTP."
            )

        if record["attempts"] >= MAX_ATTEMPTS:

            connection.execute(
                """
                DELETE FROM otp_verifications
                WHERE phone_number = ?
                """,
                (phone_number,)
            )

            connection.commit()

            raise ValueError(
                "Maximum attempts reached. "
                "Request a new OTP."
            )

        expiry_time = datetime.fromisoformat(
            record["expires_at"]
        )

        if datetime.now() > expiry_time:

            connection.execute(
                """
                DELETE FROM otp_verifications
                WHERE phone_number = ?
                """,
                (phone_number,)
            )

            connection.commit()

            raise ValueError(
                "OTP expired. Please request a new OTP."
            )

        entered_hash = hash_otp(entered_otp)

        if not hmac.compare_digest(
            entered_hash,
            record["otp_hash"]
        ):

            connection.execute(
                """
                UPDATE otp_verifications
                SET attempts = attempts + 1
                WHERE phone_number = ?
                """,
                (phone_number,)
            )

            connection.commit()

            raise ValueError(
                "Incorrect OTP. Please try again."
            )

        connection.execute(
            """
            DELETE FROM otp_verifications
            WHERE phone_number = ?
            """,
            (phone_number,)
        )

        connection.commit()

    finally:
        connection.close()

    verified = mark_phone_verified(phone_number)

    if not verified:
        raise ValueError(
            "Could not verify this mobile number."
        )

    return True
