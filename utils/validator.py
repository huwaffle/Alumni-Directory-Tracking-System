# ==========================================
# DLSAU Alumni Tracking System
# utils/validator.py
# ==========================================

import re
from datetime import datetime


def is_empty(*fields):
    """
    Returns True if any field is empty.
    """

    for field in fields:
        if str(field).strip() == "":
            return True

    return False


def is_valid_email(email):
    """
    Validates email format.
    """

    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    return re.match(pattern, email) is not None


def is_valid_student_number(student_number):
    """
    Accepts:
    - N/A (any capitalization)
    - Numbers only (6-15 digits)
    """

    student_number = student_number.strip()

    # Accept N/A regardless of capitalization
    if student_number.upper() == "N/A":
        return True

    # Otherwise, only allow 6-15 digits
    return student_number.isdigit() and 6 <= len(student_number) <= 15


def is_valid_username(username):
    """
    Username:
    - 4 to 20 characters
    - Letters, numbers, underscore
    """

    pattern = r'^[A-Za-z0-9_]{4,20}$'

    return re.match(pattern, username) is not None


def is_strong_password(password):
    """
    Minimum password requirements:
    - At least 8 characters
    """

    return len(password) >= 8


def passwords_match(password, confirm_password):
    """
    Checks if both passwords match.
    """

    return password == confirm_password


def is_valid_graduation_year(year):
    """
    Graduation year cannot be in the future.
    """

    try:

        year = int(year)

        current_year = datetime.now().year

        return 1950 <= year <= current_year

    except ValueError:
        return False