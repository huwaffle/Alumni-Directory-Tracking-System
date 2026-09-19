# ==========================================
# DLSAU Alumni Tracking System
# config.py
# ==========================================

import os

EMAIL = "amz.castalumnitracker@gmail.com"

EMAIL_PASSWORD = "hnfn qzki bbsd wief"

ADMIN_EMAIL = "amz.castalumnitracker@gmail.com"

# Theme Colors

PRIMARY_COLOR = "#00474F"
BACKGROUND_COLOR = "#FFFFFF"
TEXT_COLOR = "#000000"

# Project Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FOLDER = os.path.join(BASE_DIR, "database")

# Create database folder if it doesn't exist
os.makedirs(DATABASE_FOLDER, exist_ok=True)

# Database Path
DATABASE_NAME = "alumni.db"
DATABASE_PATH = os.path.join(DATABASE_FOLDER, DATABASE_NAME)

# System Information
SYSTEM_NAME = "DLSAU Alumni Tracking System"
SYSTEM_VERSION = "1.0"

# Default Admin Account
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin"

# User Roles
ROLE_ADMIN = "Admin"
ROLE_ALUMNI = "Alumni"

# Account Status
STATUS_PENDING = "Pending"
STATUS_APPROVED = "Approved"
STATUS_REJECTED = "Rejected"


def resolve_asset_path(path):
    """Resolve a stored asset path (which may be an old-style relative
    path like 'assets/default.png') into an absolute path anchored to
    the project directory, so image loading works no matter what the
    current working directory is when the app is launched."""

    if not path:
        return path

    if os.path.isabs(path):
        return path

    return os.path.join(BASE_DIR, path)