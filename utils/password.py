# ==========================================
# DLSAU Alumni Tracking System
# utils/password.py
# ==========================================

import hashlib


def hash_password(password):
    """
    Converts a plain-text password into a SHA-256 hash.
    """

    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hashed_password):
    """
    Checks whether the entered password matches
    the stored hashed password.
    """

    return hash_password(password) == hashed_password