# ==========================================
# DLSAU Alumni Tracking System
# models/user_model.py
# ==========================================

import sqlite3

from config import DATABASE_PATH


class UserModel:

    def __init__(self):
        self.database = DATABASE_PATH

    # ---------------------------------
    # Database Connection
    # ---------------------------------

    def connect(self):
        print("DATABASE:", self.database)
        return sqlite3.connect(self.database)

    # ---------------------------------
    # Create Alumni Account
    # ---------------------------------

    def create_user(
        self,
        student_number,
        username,
        password,
        first_name,
        middle_name,
        last_name,
        sex,
        age,
        civil_status,
        email,
        address,
        course,
        graduation_year,
        latin_honors,
        profile_picture,
        role,
        status
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users(
                student_number,
                username,
                password,
                first_name,
                middle_name,
                last_name,
                sex,
                age,
                civil_status,
                email,
                address,
                course,
                graduation_year,
                latin_honors,
                profile_picture,
                role,
                status
            )

            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (

            student_number,
            username,
            password,
            first_name,
            middle_name,
            last_name,
            sex,
            age,
            civil_status,
            email,
            address,
            course,
            graduation_year,
            latin_honors,
            profile_picture,
            role,
            status

        ))

        conn.commit()
        conn.close()

    # ---------------------------------
    # Find by Username
    # ---------------------------------

    def get_user_by_username(self, username):

        conn = self.connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()

        conn.close()

        return dict(user) if user else None

    # ---------------------------------
    # Find by Email
    # ---------------------------------

    def get_user_by_email(self, email):

        conn = self.connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        return dict(user) if user else None

    # ---------------------------------
    # Find by Student Number
    # ---------------------------------

    def get_user_by_student_number(self, student_number):

        # Allow any capitalization of N/A
        if student_number.strip().upper() == "N/A":
            return None

        conn = self.connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE student_number=?",
            (student_number,)
        )

        user = cursor.fetchone()

        conn.close()

        return dict(user) if user else None

    # ---------------------------------
    # Get User by ID
    # ---------------------------------

    def get_user_by_id(self, user_id):

        conn = self.connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE id=?",
            (user_id,)
        )

        user = cursor.fetchone()

        conn.close()

        return dict(user) if user else None

    # ---------------------------------
    # Get All Alumni
    # ---------------------------------

    def get_all_alumni(self):

        conn = self.connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE role='Alumni'
            ORDER BY last_name
        """)

        users = cursor.fetchall()

        conn.close()

        return [dict(user) for user in users]

    # =================================
    # ADMIN FUNCTIONS
    # =================================

    def get_pending_users(self):

        conn = self.connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE role='Alumni'
            AND status='Pending'
            ORDER BY last_name
        """)

        users = cursor.fetchall()

        conn.close()

        return [dict(user) for user in users]

    def get_approved_users(self):

        conn = self.connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE role='Alumni'
            AND status='Approved'
            ORDER BY last_name
        """)

        users = cursor.fetchall()

        conn.close()

        return [dict(user) for user in users]

    def get_rejected_users(self):

        conn = self.connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE role='Alumni'
            AND status='Rejected'
            ORDER BY last_name
        """)

        users = cursor.fetchall()

        conn.close()

        return [dict(user) for user in users]

    # ---------------------------------
    # Statistics
    # ---------------------------------

    def get_total_alumni(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            WHERE role='Alumni'
        """)

        count = cursor.fetchone()[0]

        conn.close()

        return count

    def get_pending_count(self):

        return len(self.get_pending_users())

    def get_approved_count(self):

        return len(self.get_approved_users())

    def get_rejected_count(self):

        return len(self.get_rejected_users())

    # ---------------------------------
    # Search
    # ---------------------------------

    def search_users(self, keyword):

        conn = self.connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        keyword = keyword.strip()

        # Search for N/A (any capitalization)
        if keyword.upper() == "N/A":

            cursor.execute("""
                SELECT *
                FROM users
                WHERE role='Alumni'
                AND student_number IS NULL
                ORDER BY last_name
            """)

        else:

            keyword = f"%{keyword}%"

            cursor.execute("""
                SELECT *
                FROM users
                WHERE role='Alumni'
                AND (
                    student_number LIKE ?
                    OR first_name LIKE ?
                    OR middle_name LIKE ?
                    OR last_name LIKE ?
                    OR username LIKE ?
                    OR email LIKE ?
                    OR course LIKE ?
                    OR graduation_year LIKE ?
                    OR status LIKE ?
                )
                ORDER BY last_name
            """,
            (
                keyword,
                keyword,
                keyword,
                keyword,
                keyword,
                keyword,
                keyword,
                keyword,
                keyword
            ))

        users = cursor.fetchall()

        conn.close()

        return [dict(user) for user in users]

    # ---------------------------------
    # Update Account Status
    # ---------------------------------

    def update_status(self, user_id, status):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(

            "UPDATE users SET status=? WHERE id=?",

            (status, user_id)

        )

        conn.commit()
        conn.close()
    
    # =================================
    # ALUMNI PROFILE FUNCTIONS
    # =================================


    # ---------------------------------
    # Check Duplicate Username
    # ---------------------------------

    def username_exists(self, username, user_id):

        print("update_user called")
        print("user_id:", user_id)
        print("username:", username)

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM users
            WHERE username=?
            AND id!=?
        """,
        (
            username,
            user_id
        ))


        result = cursor.fetchone()
        print("result:", result)

        conn.close()


        return result is not None



    # ---------------------------------
    # Check Duplicate Student Number
    # ---------------------------------

    def student_number_exists(self, student_number, user_id):

        # NULL student numbers are always allowed
        if student_number is None:
            return False

        # N/A is always allowed
        if str(student_number).strip().upper() == "N/A":
            return False

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM users
            WHERE student_number=?
            AND id!=?
        """,
        (
            student_number,
            user_id
        ))

        result = cursor.fetchone()

        conn.close()

        return result is not None



    # ---------------------------------
    # Update Alumni Profile
    # ---------------------------------

    def update_profile(
        self,
        user_id,
        student_number,
        username,
        first_name,
        middle_name,
        last_name,
        sex,
        age,
        civil_status,
        address,
        latin_honors,
        email,
        course,
        graduation_year
    ):


        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute("""
            UPDATE users

            SET

                student_number=?,
                username=?,
                first_name=?,
                middle_name=?,
                last_name=?,
                sex=?,
                age=?,
                civil_status=?,
                email=?,
                address=?,
                course=?,
                graduation_year=?,
                latin_honors=?


            WHERE id=?

        """,

        (

            student_number,
            username,
            first_name,
            middle_name,
            last_name,
            sex,
            age,
            civil_status,
            address,
            latin_honors,
            email,
            course,
            graduation_year,
            user_id

        ))


        conn.commit()

        conn.close()

    # ---------------------------------
    # Delete User
    # ---------------------------------

    def delete_user(self, user_id):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(

            "DELETE FROM users WHERE id=?",

            (user_id,)

        )

        conn.commit()
        conn.close()
        
    # ---------------------------------
    # Update Alumni Information
    # ---------------------------------

    def update_user(
        self,
        user_id,
        student_number,
        username,
        first_name,
        middle_name,
        last_name,
        sex,
        age,
        civil_status,
        address,
        latin_honors,
        email,
        course,
        graduation_year
    ):

        conn = self.connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Convert N/A to NULL
        if student_number is not None:
            if str(student_number).strip().upper() == "N/A":
                student_number = None

        if self.username_exists(username, user_id):

            conn.close()

            return False, "Username already exists."

        if self.student_number_exists(student_number, user_id):

            conn.close()

            return False, "Student number already exists."


        # -----------------------------
        # Update
        # -----------------------------
        cursor.execute(
            """
            UPDATE users
            SET
                student_number=?,
                username=?,
                first_name=?,
                middle_name=?,
                last_name=?,
                sex=?,
                age=?,
                civil_status=?,
                email=?,
                address=?,
                course=?,
                graduation_year=?,
                latin_honors=?
            WHERE id=?
            """,
            (
                student_number,
                username,
                first_name,
                middle_name,
                last_name,
                sex,
                age,
                civil_status,
                email,
                address,
                course,
                graduation_year,
                latin_honors,
                user_id
            )
        )

        conn.commit()
        conn.close()

        return True, "Updated successfully."
    
    def count_alumni(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            WHERE role='Alumni'
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total
    
    def count_approved(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            WHERE role='Alumni'
            AND status='Approved'
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total
    
    def count_pending(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            WHERE role='Alumni'
            AND status='Pending'
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total
    
    def count_employed(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM employment
            WHERE employment_status='Employed'
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total
    
    def update_profile_picture(self, user_id, picture):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""

            UPDATE users

            SET profile_picture=?

            WHERE id=?

        """,

        (

            picture,

            user_id

        ))

        conn.commit()

        conn.close()

    def get_course_summary(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT course, COUNT(*)
            FROM users
            WHERE role='Alumni'
            AND status='Approved'
            GROUP BY course
            ORDER BY course

        """)

        data = cursor.fetchall()

        conn.close()

        return data
    
    def get_graduation_year_summary(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT graduation_year, COUNT(*)
            FROM users
            WHERE role='Alumni'
            AND status='Approved'
            GROUP BY graduation_year
            ORDER BY graduation_year DESC

        """)

        data = cursor.fetchall()

        conn.close()

        return data