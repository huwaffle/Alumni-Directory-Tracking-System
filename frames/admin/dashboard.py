# ==========================================
# DLSAU Alumni Tracking System
# frames/admin/dashboard.py
# ==========================================

import tkinter as tk

from frames.base_page import BasePage
from components.button import PrimaryButton
from models.user_model import UserModel


class AdminDashboardPage(BasePage):

    def __init__(self, parent, controller):

        super().__init__(parent, controller)

        # ==========================================
        # Scrollable Canvas
        # ==========================================

        self.content = self.setup_scrollable_content()

        self.controller = controller
        self.user_model = UserModel()

        # ----------------------------
        # Title
        # ----------------------------

        self.create_title(
            "Administrator Dashboard"
        ).pack(
            in_=self.content,
            pady=30
        )

        # ----------------------------
        # System Summary
        # ----------------------------

        summary_frame = tk.Frame(
            self.content,
            bg="white",
            bd=1,
            relief="solid"
        )

        summary_frame.pack(pady=15)

        tk.Label(
            summary_frame,
            text="SYSTEM SUMMARY",
            bg="#13322B",
            fg="white",
            font=("Helvetica", 15, "bold"),
            width=40,
            pady=8
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        self.summary_labels = {}

        summary_items = [

            "Total Alumni",
            "Approved Alumni",
            "Pending Approval",
            "Rejected Alumni"

        ]

        for row, item in enumerate(summary_items, start=1):

            tk.Label(

                summary_frame,

                text=item,

                width=25,

                anchor="w",

                bg="#D6DEDC",

                font=("Helvetica", 14, "bold"),

                padx=10,

                pady=8

            ).grid(

                row=row,

                column=0,

                sticky="nsew"

            )

            value = tk.Label(

                summary_frame,

                text="0",

                width=12,

                bg="white",

                anchor="center",

                font=("Helvetica", 14)

            )

            value.grid(

                row=row,

                column=1,

                sticky="nsew"

            )

            self.summary_labels[item] = value

        # ----------------------------
        # Course Summary
        # ----------------------------

        course_frame = tk.Frame(
            self.content,
            bg="white",
            bd=1,
            relief="solid"
        )

        course_frame.pack(pady=15)

        tk.Label(
            course_frame,
            text="COURSE SUMMARY",
            bg="#13322B",
            fg="white",
            font=("Helvetica", 15, "bold"),
            width=40,
            pady=8
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        self.course_frame = course_frame
        self.course_labels = {}

            
        # ----------------------------
        # Graduation Year Summary
        # ----------------------------

        year_frame = tk.Frame(
            self.content,
            bg="white",
            bd=1,
            relief="solid"
        )

        year_frame.pack(pady=15)

        tk.Label(
            year_frame,
            text="GRADUATION YEAR SUMMARY",
            bg="#13322B",
            fg="white",
            font=("Helvetica", 15, "bold"),
            width=40,
            pady=8
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        self.year_frame = year_frame
        self.year_labels = {}


        # ----------------------------
        # Buttons
        # ----------------------------

        PrimaryButton(
            self.content,
            "Manage Alumni",
            lambda: controller.show_frame(
                "ManageAlumniPage"
            )
        ).pack(pady=20)

        PrimaryButton(
            self.content,
            text="Logout",
            command=lambda: controller.show_frame(
                "WelcomePage"
            )
        ).pack()

        self.refresh_statistics()

    # ======================================

    def refresh_statistics(self):

        self.summary_labels["Total Alumni"].config(
            text=self.user_model.get_total_alumni()
        )

        self.summary_labels["Approved Alumni"].config(
            text=self.user_model.get_approved_count()
        )

        self.summary_labels["Pending Approval"].config(
            text=self.user_model.get_pending_count()
        )

        self.summary_labels["Rejected Alumni"].config(
            text=self.user_model.get_rejected_count()
        )

        self.refresh_course_summary()
        self.refresh_year_summary()
    
    def refresh_course_summary(self):

        # Delete old labels
        for widget in self.course_frame.grid_slaves():

            info = widget.grid_info()

            if info["row"] != 0:
                widget.destroy()

        courses = self.user_model.get_course_summary()

        for row, (course, count) in enumerate(courses, start=1):

            tk.Label(
                self.course_frame,
                text=course,
                width=25,
                anchor="w",
                bg="#D6DEDC",
                font=("Helvetica", 14, "bold"),
                padx=10,
                pady=8
            ).grid(row=row, column=0, sticky="nsew")

            tk.Label(
                self.course_frame,
                text=str(count),
                width=12,
                bg="white",
                font=("Helvetica", 14)
            ).grid(row=row, column=1, sticky="nsew")

    def refresh_year_summary(self):

        for widget in self.year_frame.grid_slaves():

            info = widget.grid_info()

            if info["row"] != 0:
                widget.destroy()

        years = self.user_model.get_graduation_year_summary()

        for row, (year, count) in enumerate(years, start=1):

            tk.Label(
                self.year_frame,
                text=year,
                width=25,
                anchor="w",
                bg="#D6DEDC",
                font=("Helvetica", 14, "bold"),
                padx=10,
                pady=8
            ).grid(row=row, column=0, sticky="nsew")

            tk.Label(
                self.year_frame,
                text=str(count),
                width=12,
                bg="white",
                font=("Helvetica", 14)
            ).grid(row=row, column=1, sticky="nsew")

    def bind_mousewheel(self, event):

        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )


    def unbind_mousewheel(self, event):

        self.canvas.unbind_all(
            "<MouseWheel>"
        )


    def on_mousewheel(self, event):

        self.canvas.yview_scroll(
            -int(event.delta / 120),
            "units"
        )


    def resize_content(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )