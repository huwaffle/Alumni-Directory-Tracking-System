
# ==========================================
# DLSAU Alumni Tracking System
# frames/alumni/employment.py
# ==========================================

from tkinter import ttk
from components.button import PrimaryButton

import tkinter as tk

from frames.base_page import BasePage

from models.employment_model import EmploymentModel

from utils.session import get_user


class EmploymentPage(BasePage):

    def __init__(self, parent, controller):

        self.editing = False

        super().__init__(parent, controller)

        self.controller = controller
        self.model = EmploymentModel()

        self.form_frame = tk.Frame(
            self,
            bg=self.BG_COLOR
        )

        self.form_frame.place(
            relx=0.5,
            rely=0.45,
            anchor="center"
        )

        self.table = tk.Frame(
            self.form_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        self.table.pack()

        tk.Label(
            self.table,
            text="Employment Information",
            bg="white",
            fg="#13322B",
            font=("PT Serif", 24, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(20, 15)
        )

        self.table.grid_columnconfigure(
            0,
            weight=0
        )

        self.table.grid_columnconfigure(
            1,
            weight=1
        )

        self.entries = {}

        self.fields = [

            ("EMPLOYMENT INFORMATION", None),

            ("Employment Status", "employment_status"),
            ("Company", "company"),
            ("Job Title", "job_title"),
            ("Industry", "industry"),
            ("Work Location", "work_location"),
            ("Salary Range", "salary_range")

        ]

        row = 1

        for title, key in self.fields:

            if key is None:

                tk.Label(
                    self.table,
                    text=title,
                    bg="#13322B",
                    fg="white",
                    font=("Helvetica", 14, "bold"),
                    pady=8
                ).grid(
                    row=row,
                    column=0,
                    columnspan=2,
                    sticky="ew",
                    pady=(10,2)
                )

                row += 1
                continue

            tk.Label(
                self.table,
                text=title,
                width=24,
                anchor="w",
                bg="#D6DEDC",
                font=("Helvetica", 14, "bold"),
                padx=10,
                pady=10
            ).grid(
                row=row,
                column=0,
                sticky="nsew"
            )

            if key == "employment_status":

                entry = ttk.Combobox(
                    self.table,
                    width=37,
                    state="readonly",
                    values=[
                        "Employed (Full-time)",
                        "Employed (Part-time)",
                        "Self-employed",
                        "Freelancer",
                        "Unemployed but seeking work",
                        "Unemployed and not seeking work",
                        "Pursuing further studies"
                    ]
                )

            elif key == "salary_range":

                entry = ttk.Combobox(
                    self.table,
                    width=37,
                    state="readonly",
                    values=[
                        "Below ₱20,000",
                        "₱20,000 - ₱39,999",
                        "₱40,000 - ₱59,999",
                        "₱60,000 - ₱79,999",
                        "₱80,000 and above",
                        "Prefer not to answer"
                    ]
                )

            else:

                entry = tk.Entry(
                    self.table,
                    width=40
                )

            entry.grid(
                row=row,
                column=1,
                sticky="ew",
                padx=8,
                pady=6
            )

            self.entries[key] = entry

            row += 1

        self.load_data()

        # ==========================================
        # Buttons
        # ==========================================

        button_frame = tk.Frame(
            self.form_frame,
            bg=self.BG_COLOR
        )

        button_frame.pack(pady=20)

        self.edit_button = PrimaryButton(
            button_frame,
            "Edit Employment",
            self.enable_editing
        )

        self.edit_button.grid(
            row=0,
            column=0,
            padx=5
        )

        self.save_button = PrimaryButton(
            button_frame,
            "Save",
            self.save
        )

        self.cancel_button = PrimaryButton(
            button_frame,
            "Cancel",
            self.cancel_edit
        )

        PrimaryButton(
            button_frame,
            "Back",
            lambda: controller.show_frame(
                "AlumniDashboardPage"
            )
        ).grid(
            row=0,
            column=3,
            padx=5
        )

    # ---------------------------------

    def load_data(self):

        user = get_user()

        if not user:
            return

        data = self.model.get_employment(user["id"])

        if not data:
            return

        for key, entry in self.entries.items():

            if isinstance(entry, ttk.Combobox):
                entry.set(data.get(key, ""))
            else:
                entry.delete(0, tk.END)
                entry.insert(0, data.get(key, ""))

        for entry in self.entries.values():

            if isinstance(entry, ttk.Combobox):
                entry.config(state="disabled")
            else:
                entry.config(state="readonly")

    # ---------------------------------

    def save(self):

        user = get_user()

        if not user:
            return

        self.model.save_employment(

            user["id"],

            self.entries["employment_status"].get(),

            self.entries["company"].get(),

            self.entries["job_title"].get(),

            self.entries["industry"].get(),

            self.entries["work_location"].get(),

            self.entries["salary_range"].get()

        )

        self.toast_success("Employment information saved.")

        self.cancel_edit()

    def enable_editing(self):

        self.editing = True

        for entry in self.entries.values():

            if isinstance(entry, ttk.Combobox):
                entry.config(state="readonly")
            else:
                entry.config(state="normal")

        self.edit_button.grid_remove()

        self.save_button.grid(
            row=0,
            column=0,
            padx=5
        )

        self.cancel_button.grid(
            row=0,
            column=1,
            padx=5
        )

    def cancel_edit(self):

        self.editing = False

        self.load_data()

        self.save_button.grid_remove()
        self.cancel_button.grid_remove()

        self.edit_button.grid(
            row=0,
            column=0,
            padx=5
        )
    