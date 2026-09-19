# ==========================================
# DLSAU Alumni Tracking System
# database.py
# ==========================================

import sqlite3
from config import *


# ------------------------------------------
# Connect to Database
# ------------------------------------------

def connect():
    return sqlite3.connect(DATABASE_PATH)


# ------------------------------------------
# Hash Password
# (Temporary - later we'll move this to
# utils/password.py)
# ------------------------------------------

from utils.password import hash_password


# ------------------------------------------
# Initialize Database
# ------------------------------------------

def initialize_database():

    conn = connect()
    cursor = conn.cursor()

    # ======================================
    # USERS TABLE
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        student_number TEXT UNIQUE,
        username TEXT UNIQUE,
        password TEXT,

        first_name TEXT,
        middle_name TEXT,
        last_name TEXT,

        sex TEXT,
        age TEXT,
        civil_status TEXT,

        email TEXT,
        address TEXT,

        course TEXT,
        graduation_year TEXT,
        latin_honors TEXT,

        profile_picture TEXT DEFAULT 'assets/default.png',
        
        role TEXT,
        status TEXT
    )
    """)

    # ==========================================
    # Employment Information
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employment(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER UNIQUE,

        employment_status TEXT,

        company TEXT,

        job_title TEXT,

        industry TEXT,

        work_location TEXT,

        salary_range TEXT,

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )
    """)

    # ======================================
    # EVENTS TABLE
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT NOT NULL,

        description TEXT,

        event_date TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ======================================
    # ANNOUNCEMENTS TABLE
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS announcements(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT NOT NULL,

        content TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ======================================
    # EMPLOYMENT TABLE
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employment(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        company TEXT,

        job_title TEXT,

        employment_status TEXT,

        salary TEXT,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)

    # ======================================
    # CREATE DEFAULT ADMIN
    # ======================================

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (DEFAULT_ADMIN_USERNAME,)
    )

    admin = cursor.fetchone()

    if admin is None:

        cursor.execute("""
        INSERT INTO users(

            student_number,
            username,
            password,
            first_name,
            middle_name,
            last_name,
            email,
            course,
            graduation_year,
            role,
            status

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?)
        """,

        (

            "ADMIN",

            DEFAULT_ADMIN_USERNAME,

            hash_password(DEFAULT_ADMIN_PASSWORD),

            "System",

            "",

            "Administrator",

            "admin@dlsau.local",

            "Administration",

            2025,

            ROLE_ADMIN,

            STATUS_APPROVED

        ))

    conn.commit()
    conn.close()


# ------------------------------------------
# Test Database
# ------------------------------------------

if __name__ == "__main__":

    initialize_database()

    print("Database created successfully!")