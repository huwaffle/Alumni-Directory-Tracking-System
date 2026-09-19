# ==========================================
# DLSAU Alumni Tracking System
# frames/admin/alumni_details.py
# ==========================================

from PIL import Image, ImageTk
import os

import tkinter as tk
from tkinter import ttk

from components.button import PrimaryButton

from frames.base_page import BasePage

from models.user_model import UserModel

from models.employment_model import EmploymentModel

from config import resolve_asset_path

from utils.session import (
    get_selected_alumni,
    set_selected_alumni
)


class AlumniDetailsPage(BasePage):

    def __init__(self, parent, controller):

        super().__init__(parent, controller)

        self.controller = controller
        self.user_model = UserModel()
        self.employment_model = EmploymentModel()

        self.user = None
        self.edit_mode = False

        self.entries = {}
        self.value_labels = {}

        # ==========================
        # Scrollable Canvas
        # ==========================

        shell = self.create_content_pane()

        self.canvas = tk.Canvas(
            shell,
            bg=self.BG_COLOR,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            shell,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.content = tk.Frame(
            self.canvas,
            bg=self.BG_COLOR
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="n"
        )

        self.content.bind(
            "<Configure>",
            lambda e:
            self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_content
        )

        # Mouse Wheel
        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

        tk.Label(
            self.content,
            text="Alumni Details",
            font=("Helvetica", 24, "bold"),
            bg=self.BG_COLOR
        ).pack(
            pady=20
        )

        # ==========================
        # Profile Picture
        # ==========================

        self.photo_label = tk.Label(
            self.content,
            bg=self.BG_COLOR,
            width=180,
            height=180
        )

        self.photo_label.pack(
            pady=(0, 15)
        )

        PrimaryButton(
            self.content,
            "Reset Profile Picture",
            self.reset_profile_picture
        ).pack(pady=(0, 15))

        # ==========================
        # Table
        # ==========================

        self.table = tk.Frame(
            self.content,
            bg="white",
            bd=1,
            relief="solid"
        )

        self.table.pack(
            pady=15,
            anchor="center"
        )

        self.fields = [

            ("PERSONAL INFORMATION", None),

            ("Student Number", "student_number"),
            ("Username", "username"),
            ("First Name", "first_name"),
            ("Middle Name", "middle_name"),
            ("Last Name", "last_name"),

            ("Sex", "sex"),
            ("Age", "age"),
            ("Civil Status", "civil_status"),
            ("Address", "address"),

            ("Email", "email"),

            ("ACADEMIC INFORMATION", None),

            ("Course", "course"),
            ("Graduation Year", "graduation_year"),
            ("Latin Honors", "latin_honors"),

            ("EMPLOYMENT INFORMATION", None),

            ("Employment Status", "employment_status"),
            ("Company", "company"),
            ("Job Title", "job_title"),
            ("Industry", "industry"),
            ("Work Location", "work_location"),
            ("Salary Range", "salary_range"),

            ("ACCOUNT INFORMATION", None),

            ("Role", "role"),
            ("Status", "status")

        ]

        row = 0

        for title, key in self.fields:

            tk.Label(

                self.table,

                text=title,

                width=22,

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

                self.table,

                text="",

                width=35,

                anchor="w",

                bg="white",

                padx=10,
                pady=8

            )

            value.grid(
                row=row,
                column=1,
                sticky="nsew"
            )

            self.value_labels[key] = value

            row += 1

        # ==========================
        # Buttons
        # ==========================

        self.button_frame = tk.Frame(
            self.content,
            bg=self.BG_COLOR
        )

        self.button_frame.pack(pady=20)

        self.edit_button = PrimaryButton(
            self.button_frame,
            "Edit",
            self.enable_edit
        )

        self.edit_button.pack(
            side="left",
            padx=10
        )

        self.back_button = PrimaryButton(
            self.button_frame,
            "Back",
            lambda: controller.show_frame("ManageAlumniPage")
        )

        self.back_button.pack(
            side="left",
            padx=10
        )

    # ======================================

    def load_profile(self):

        self.user = get_selected_alumni()

        employment = self.employment_model.get_employment(
            self.user["id"]
        )

        if employment:
            self.user.update(employment)

        # ==========================
        # Load Profile Picture
        # ==========================

        image_path = resolve_asset_path(
            self.user.get("profile_picture", "assets/default.png")
        )

        if not os.path.exists(image_path):
            image_path = resolve_asset_path("assets/default.png")

        image = Image.open(image_path)

        image = image.resize(
            (180, 180)
        )

        self.photo = ImageTk.PhotoImage(image)

        self.photo_label.configure(
            image=self.photo,
            text=""
        )

        if not self.user:
            return

        self.disable_edit()

    # ======================================

    # ======================================

    def disable_edit(self):

        self.edit_mode = False

        for widget in self.table.grid_slaves():
            widget.destroy()

        self.value_labels = {}

        row = 0

        for title, key in self.fields:

            # -----------------------------
            # Section Header
            # -----------------------------
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

                    pady=(10, 2)

                )

                row += 1
                continue

            # -----------------------------
            # Field Name
            # -----------------------------
            tk.Label(

                self.table,

                text=title,

                width=22,

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

            print(key, "=", self.user.get(key, "NOT FOUND"))

            display_value = self.user.get(key)

            # Display N/A if the student number is NULL
            if key == "student_number" and display_value is None:
                display_value = "N/A"

            label = tk.Label(
                self.table,
                text=display_value if display_value is not None else "",
                width=35,
                anchor="w",
                bg="white",
                padx=10,
                pady=8
            )

            label.grid(
                row=row,
                column=1,
                sticky="nsew"
            )

            self.value_labels[key] = label

            row += 1

        self.edit_button.config(
            text="Edit",
            command=self.enable_edit
        )

        self.back_button.config(
            text="Back",
            command=lambda:
            self.controller.show_frame(
                "ManageAlumniPage"
            )
        )

    # ======================================

    # ======================================

    def enable_edit(self):

        self.edit_mode = True

        # Clear existing table
        for widget in self.table.grid_slaves():
            widget.destroy()

        self.entries = {}

        row = 0

        for title, key in self.fields:

            # -----------------------------
            # Section Headers
            # -----------------------------
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
                    pady=(10, 2)
                )

                row += 1
                continue

            # -----------------------------
            # Field Name
            # -----------------------------
            tk.Label(
                self.table,
                text=title,
                width=22,
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

            # -----------------------------
            # Read-only fields
            # -----------------------------
            if key in ["role", "status"]:

                tk.Label(
                    self.table,
                    text=self.user.get(key, ""),
                    width=35,
                    anchor="w",
                    bg="white",
                    padx=10,
                    pady=8
                ).grid(
                    row=row,
                    column=1,
                    sticky="nsew"
                )

            else:

                # -----------------------------
                # Dropdown Fields
                # -----------------------------
                if key == "sex":

                    entry = ttk.Combobox(
                        self.table,
                        width=37,
                        state="readonly",
                        values=[
                            "Male",
                            "Female"
                        ]
                    )

                elif key == "age":

                    entry = ttk.Combobox(
                        self.table,
                        width=37,
                        state="readonly",
                        values=[
                            "Below 21",
                            "21-25",
                            "26-30",
                            "31 above"
                        ]
                    )

                elif key == "civil_status":

                    entry = ttk.Combobox(
                        self.table,
                        width=37,
                        state="readonly",
                        values=[
                            "Single",
                            "Married",
                            "Widowed",
                            "Prefer not to say"
                        ]
                    )

                elif key == "course":

                    entry = ttk.Combobox(
                        self.table,
                        width=37,
                        state="readonly",
                        values=[
                            "BSCS",
                            "BSCoE",
                            "ABPsych"
                        ]
                    )

                elif key == "latin_honors":

                    entry = ttk.Combobox(
                        self.table,
                        width=37,
                        state="readonly",
                        values=[
                            "Summa Cum Laude",
                            "Magna Cum Laude",
                            "Cum Laude"
                        ]
                    )

                elif key == "employment_status":

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

                # Set current value
                value = self.user.get(key)

                # Show N/A if student number is NULL
                if key == "student_number" and value is None:
                    value = "N/A"

                if value is None:
                    value = ""

                if isinstance(entry, ttk.Combobox):

                    entry.set(value)

                else:

                    entry.insert(0, value)

                entry.grid(
                    row=row,
                    column=1,
                    sticky="ew",
                    padx=5,
                    pady=5
                )

                self.entries[key] = entry

            row += 1

        # -----------------------------
        # Buttons
        # -----------------------------
        self.edit_button.config(
            text="Save",
            command=self.save_changes
        )

        self.back_button.config(
            text="Cancel",
            command=self.disable_edit
        )
        
    # ======================================

    def save_changes(self):

        updated = {}

        for key, entry in self.entries.items():

            value = entry.get().strip()

            if key == "student_number" and value.upper() == "N/A":
                value = None

            if value == "":
                value = self.user.get(key, "")

            updated[key] = value

        # Update database

        success, message = self.user_model.update_user(

            self.user["id"],

            updated["student_number"],
            updated["username"],
            updated["first_name"],
            updated["middle_name"],
            updated["last_name"],

            updated["sex"],
            updated["age"],
            updated["civil_status"],
            updated["address"],
            updated["latin_honors"],

            updated["email"],
            updated["course"],
            updated["graduation_year"]

        )

        self.employment_model.save_employment(

            self.user["id"],

            updated["employment_status"],

            updated["company"],

            updated["job_title"],

            updated["industry"],

            updated["work_location"],

            updated["salary_range"]

)

        if not success:

            self.toast_error(message, "Update Failed")

            return

        # Reload user
        self.user = self.user_model.get_user_by_id(
            self.user["id"]
        )

        # Reload employment
        employment = self.employment_model.get_employment(
            self.user["id"]
        )

        if employment:
            self.user.update(employment)

        set_selected_alumni(self.user)

        self.toast_success("Alumni information updated successfully.")

        self.disable_edit()

        # ======================================


    def on_mousewheel(self, event):

        self.canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"

        )

        
    def resize_content(self, event):
        self.canvas.itemconfig(
        self.canvas_window,
        width=event.width
    )
        
    def reset_profile_picture(self):

        path = self.user.get(
            "profile_picture",
            "assets/default.png"
        )

        if (
            path != "assets/default.png"
            and
            os.path.exists(resolve_asset_path(path))
        ):

            os.remove(resolve_asset_path(path))

        self.user_model.update_profile_picture(

            self.user["id"],

            "assets/default.png"

        )

        self.user["profile_picture"] = "assets/default.png"

        self.load_profile()

        self.toast_success("Profile picture has been reset.")
