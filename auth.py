# ==========================================
# DLSAU Alumni Tracking System
# auth.py
# ==========================================

from models.user_model import UserModel

from utils.password import (
    hash_password,
    verify_password
)

from utils.validator import *

from utils.session import login

from config import *

from utils.email_sender import send_email


class Auth:

    def __init__(self):
        self.user_model = UserModel()

    # ---------------------------------
    # Register Alumni
    # ---------------------------------

    def register(
        self,
        student_number,
        username,
        password,
        confirm_password,
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
        profile_picture
    ):
        
        # ---------------------------------
        # Normalize Student Number
        # ---------------------------------

        student_number = student_number.strip()

        if student_number.upper() == "N/A":
            student_number = None

        # Empty fields
        if is_empty(
            student_number,
            username,
            password,
            confirm_password,
            first_name,
            last_name,
            sex,
            age,
            civil_status,
            email,
            address,
            course,
            graduation_year,
            latin_honors,
            profile_picture
        ):
                
            return False, "Please fill in all required fields."

        # Student Number
        if student_number is not None:
            if not is_valid_student_number(student_number):
                return False, "Invalid student number."

        # Username
        if not is_valid_username(username):
            return False, "Username must be 4-20 characters."

        # Email
        if not is_valid_email(email):
            return False, "Invalid email address."

        # Password
        if not is_strong_password(password):
            return False, "Password must be at least 8 characters."

        # Confirm Password
        if not passwords_match(password, confirm_password):
            return False, "Passwords do not match."

        # Graduation Year
        if not is_valid_graduation_year(graduation_year):
            return False, "Invalid graduation year."

        # Duplicate Checks
        if self.user_model.get_user_by_username(username):
            return False, "Username already exists."

        if self.user_model.get_user_by_email(email):
            return False, "Email already exists."

        if student_number is not None:
            if self.user_model.get_user_by_student_number(student_number):
                return False, "Student number already exists."

        # Create User
        self.user_model.create_user(
            student_number,
            username,
            hash_password(password),
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
            ROLE_ALUMNI,
            STATUS_PENDING
        )

        # ---------------------------------
        # Notify Admin
        # ---------------------------------

        subject = "New Alumni Registration"

        body = f"""
        A new alumni has registered and is waiting for approval.

        Name:
        {first_name} {last_name}

        Student Number:
        {student_number if student_number else "N/A"}

        Course:
        {course}

        Graduation Year:
        {graduation_year}

        Please log in to the Alumni Tracking System to review the registration.

        Group 2 Development Team
        """

        send_email(
            ADMIN_EMAIL,
            subject,
            body
        )

        return True, "Registration successful! Please wait for admin approval."

    # ---------------------------------
    # Login
    # ---------------------------------

    def login(self, username, password):

        user = self.user_model.get_user_by_username(username)

        if user is None:
            return False, "Invalid username or password."

        if not verify_password(password, user["password"]):
            return False, "Invalid username or password."

        if user["role"] == ROLE_ALUMNI:

            if user["status"] == STATUS_PENDING:
                return False, "Your account is pending approval."

            if user["status"] == STATUS_REJECTED:
                return False, "Your account has been rejected."

        # Save Session
        login(user)

        return True, user