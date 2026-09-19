# ==========================================
# DLSAU Alumni Tracking System
# frames/alumni_login.py
# ==========================================

import tkinter as tk

from frames.base_page import BasePage

from components.button import PrimaryButton
from components.entry import PrimaryEntry

from auth import Auth

from utils.session import login


class AlumniLoginPage(BasePage):

    def __init__(self, parent, controller):

        super().__init__(parent, controller)

        self.controller = controller
        self.auth = Auth()

        # =========================
        # Center Container
        # =========================

        container = tk.Frame(
            self,
            bg=self.BG_COLOR
        )

        container.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # =========================
        # Page Title
        # =========================

        tk.Label(
            container,
            text="DLSAU Alumni Tracking System",
            bg=self.BG_COLOR,
            font=("PT Serif", 28, "bold")
        ).pack(pady=(0,30))

        # =========================
        # Login Card
        # =========================

        login_card = tk.Frame(
            container,
            bg="white",
            bd=1,
            relief="solid",
            padx=20,
            pady=20
        )

        login_card.pack()

        # =========================
        # Inner Content
        # =========================

        content = tk.Frame(
            login_card,
            bg="white"
        )

        content.pack(
            padx=40,
            pady=30
        )

        # =========================
        # Card Title
        # =========================

        tk.Label(
            content,
            text="Alumni Login",
            bg="white",
            fg="#13322B",
            font=("PT Serif", 20, "bold")
        ).pack(pady=(0,20))

        # =========================
        # Username
        # =========================

        tk.Label(
            content,
            text="Username",
            bg="white",
            font=("Helvetica", 14, "bold")
        ).pack(anchor="w")

        self.username_entry = PrimaryEntry(content)

        self.username_entry.pack(
            fill="x",
            pady=(5,15)
        )

        # =========================
        # Password
        # =========================

        tk.Label(
            content,
            text="Password",
            bg="white",
            font=("Helvetica", 14, "bold")
        ).pack(anchor="w")

        self.password_entry = PrimaryEntry(
            content,
            show="*"
        )

        self.password_entry.pack(
            fill="x",
            pady=(5,20)
        )

        # =========================
        # Buttons
        # =========================

        button_frame = tk.Frame(
            content,
            bg="white"
        )

        button_frame.pack(pady=(10,0))

        PrimaryButton(
            button_frame,
            "Login",
            self.login
        ).pack(side="left", padx=5)

        PrimaryButton(
            button_frame,
            "Back",
            lambda: controller.show_frame("WelcomePage")
        ).pack(side="left", padx=5)

    # ================================


    def login(self):

        username = self.username_entry.get()

        password = self.password_entry.get()


        success, result = self.auth.login(
            username,
            password
        )


        if not success:

            self.toast_error(result, "Login Failed")

            return


        # Check if account is Alumni

        if result["role"] != "Alumni":

            self.toast_error(
                "This account is not an alumni account.",
                "Access Denied"
            )

            return


        # Check approval status

        if result["status"] != "Approved":

            self.toast_warning(
                "Your account is not approved yet.",
                "Account Pending"
            )

            return


        # Save session

        login(result)


        self.toast_success(f"Welcome {result['first_name']}!")


        self.controller.show_frame(
            "AlumniDashboardPage"
        )