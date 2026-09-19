# ==========================================
# DLSAU Alumni Tracking System
# frames/alumni/dashboard.py
# ==========================================

import tkinter as tk

from frames.base_page import BasePage

from components.button import PrimaryButton

from utils.session import get_user, logout


class AlumniDashboardPage(BasePage):

    def __init__(self, parent, controller):

        super().__init__(parent, controller)

        self.controller = controller

        # ==========================
        # Center Container
        # ==========================

        container = tk.Frame(
            self,
            bg=self.BG_COLOR
        )

        container.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # ==========================
        # Dashboard Card
        # ==========================

        card = tk.Frame(
            container,
            bg="white",
            bd=1,
            relief="solid",
            width=600,
            height=400
        )

        card.pack()
        card.pack_propagate(False)

        content = tk.Frame(
            card,
            bg="white"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=30
        )

        self.title = tk.Label(
            content,
            text="Alumni Dashboard",
            bg="white",
            fg="#13322B",
            font=("PT Serif", 24, "bold")
        )

        self.title.pack(pady=(0, 20))

        self.name_label = tk.Label(
            content,
            bg="white",
            font=("Helvetica", 17, "bold")
        )

        self.name_label.pack()

        self.status_label = tk.Label(
            content,
            bg="white",
            fg="#3F4947",
            font=("Helvetica", 15)
        )

        self.status_label.pack(pady=(5, 20))

        # BUTTON ====================

        PrimaryButton(
            content,
            "My Profile",
            lambda: self.controller.show_frame("AlumniProfilePage")
        ).pack(pady=8)

        PrimaryButton(
            content,
            "Employment Information",
            lambda: self.controller.show_frame("EmploymentPage")
        ).pack(pady=8)

        PrimaryButton(
            content,
            "Logout",
            self.logout
        ).pack(pady=8)

    # ======================================

    def refresh_profile(self):

        user = get_user()

        if user:

            fullname = (
                user["first_name"]
                + " "
                + user["last_name"]
            )

            self.name_label.config(
                text=f"Welcome, {fullname}"
            )

            self.status_label.config(
                text=f"Account Status: {user['status']}"
            )

    # ======================================

    def logout(self):

        logout()

        self.controller.show_frame(
            "WelcomePage"
        )