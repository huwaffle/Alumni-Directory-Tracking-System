# ==========================================
# DLSAU Alumni Tracking System
# frames/alumni/profile.py
# ==========================================

from tkinter import filedialog
from PIL import Image, ImageTk
import shutil
import os

from tkinter import ttk

from components.button import PrimaryButton

import tkinter as tk

from frames.base_page import BasePage

from utils.session import get_user, login

from models.user_model import UserModel

from config import resolve_asset_path


class AlumniProfilePage(BasePage):

    def __init__(self, parent, controller):

        super().__init__(parent, controller)

        # ==========================================
        # Scrollable Canvas
        # ==========================================

        self.content = self.setup_scrollable_content()

        self.controller = controller
        self.user_model = UserModel()

        self.editing = False

        # ==========================
        # Form Frame
        # ==========================

        self.form_frame = tk.Frame(
            self.content,
            bg=self.BG_COLOR
        )

        self.form_frame.pack(
            pady=20
        )

        self.table = tk.Frame(
            self.form_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        self.table.pack()

        # ==========================================
        # Header inside table
        # ==========================================

        tk.Label(
            self.table,
            text="My Profile",
            bg="white",
            fg="#13322B",
            font=("PT Serif", 24, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(20,10)
        )

        self.profile_label = tk.Label(
            self.table,
            bg="white"
        )

        self.profile_label.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=(0,15)
        )

        self.change_picture_button = PrimaryButton(
            self.table,
            "Change Profile Picture",
            self.change_profile_picture
        )

        self.remove_picture_button = PrimaryButton(
            self.table,
            "Remove Profile Picture",
            self.remove_profile_picture
        )

        # hidden until editing
        self.change_picture_button.grid_forget()
        self.remove_picture_button.grid_forget()

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

        ]

        row = 3

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
            # Left Column
            # -----------------------------
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

            # -----------------------------
            # Right Column
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
                        "Above 35"
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
                        "Cum Laude",
                        "None"
                    ]
                )

            elif key == "graduation_year":

                years = [str(year) for year in range(2026, 1989, -1)]

                entry = ttk.Combobox(
                    self.table,
                    width=37,
                    state="readonly",
                    values=years
                )

            elif key == "address":

                entry = tk.Text(
                    self.table,
                    width=35,
                    height=3,
                    font=("Helvetica", 14)
                )

                entry.config(state="disabled")

            else:

                entry = tk.Entry(
                    self.table,
                    width=40
                )

                entry.config(state="readonly")

            entry.grid(
                row=row,
                column=1,
                sticky="ew",
                padx=8,
                pady=6
            )

            self.entries[key] = entry

            row += 1

        # =============================
        # BUTTONS
        # =============================

        button_frame = tk.Frame(
            self.content,
            bg=self.BG_COLOR
        )

        button_frame.pack(pady=20)

        self.edit_button = PrimaryButton(
            button_frame,
            "Edit Profile",
            self.enable_editing
        )

        self.edit_button.grid(
            row=0,
            column=0,
            padx=5
        )

        self.save_button = PrimaryButton(
            button_frame,
            "Save Changes",
            self.save_profile
        )

        self.cancel_button = PrimaryButton(
            button_frame,
            "Cancel",
            self.cancel_edit
        )

        PrimaryButton(
            self.content,
            "Back",
            lambda: controller.show_frame(
                "AlumniDashboardPage"
            )
        ).pack(pady=(0, 20))

        self.load_profile()
        self.load_profile_picture()

    # ==========================================
    # Load Profile
    # ==========================================

    def load_profile(self):

        user = get_user()

        if not user:
            return

        self.load_profile_picture()

        for field, entry in self.entries.items():

            value = user.get(field)

            # Show N/A if student number is NULL
            if field == "student_number" and value is None:
                value = "N/A"

            # Prevent None from being inserted into widgets
            if value is None:
                value = ""

            if field == "address":

                entry.config(state="normal")
                entry.delete("1.0", tk.END)
                entry.insert("1.0", value)

                if not self.editing:
                    entry.config(state="disabled")

            else:

                entry.config(state="normal")

                if isinstance(entry, ttk.Combobox):
                    entry.set(value)
                else:
                    entry.delete(0, tk.END)
                    entry.insert(0, value)

                if not self.editing:

                    if isinstance(entry, ttk.Combobox):
                        entry.config(state="disabled")
                    else:
                        entry.config(state="readonly")

    # =============================
    def load_profile_picture(self):

        user = get_user()

        if not user:
            return
        
        picture = user.get("profile_picture")
        picture = resolve_asset_path(picture)

        if not picture or not os.path.exists(picture):
            picture = resolve_asset_path("assets/default.png")

        image = Image.open(picture)
        image = image.resize((150,150))

        self.photo = ImageTk.PhotoImage(image)

        self.profile_label.config(
            image=self.photo
        )

    # ==========================================
    # Enable Editing
    # ==========================================

    def enable_editing(self):

        self.change_picture_button.grid(
            row=2,
            column=0,
            padx=5,
            pady=(0,10),
            sticky="e"
        )

        self.remove_picture_button.grid(
            row=2,
            column=1,
            padx=5,
            pady=(0,10),
            sticky="w"
        )

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

    # ==========================================
    # Cancel Editing
    # ==========================================

    def cancel_edit(self):

        self.change_picture_button.grid_forget()
        self.remove_picture_button.grid_forget()

        self.editing = False

        self.load_profile()

        self.save_button.grid_remove()
        self.cancel_button.grid_remove()

        self.edit_button.grid(
            row=0,
            column=0,
            padx=5
        )

    # ==========================================
    # Save Profile
    # ==========================================

    def save_profile(self):

        user = get_user()

        if not user:
            return

        student_number = self.entries["student_number"].get().strip()
        if student_number.upper() == "N/A":
            student_number = None
        username = self.entries["username"].get().strip()
        first_name = self.entries["first_name"].get().strip()
        middle_name = self.entries["middle_name"].get().strip()
        last_name = self.entries["last_name"].get().strip()
        sex = self.entries["sex"].get().strip()

        age = self.entries["age"].get().strip()

        civil_status = self.entries["civil_status"].get().strip()

        address = self.entries["address"].get(
            "1.0",
            "end-1c"
        ).strip()

        latin_honors = self.entries["latin_honors"].get().strip()
        email = self.entries["email"].get().strip()
        course = self.entries["course"].get().strip()
        graduation_year = self.entries["graduation_year"].get().strip()

        # Keep original value if blank

        if student_number == "":
            student_number = user["student_number"]

        if username == "":
            username = user["username"]

        if first_name == "":
            first_name = user["first_name"]

        if last_name == "":
            last_name = user["last_name"]

        if sex == "":
            sex = user["sex"]

        if age == "":
            age = user["age"]

        if civil_status == "":
            civil_status = user["civil_status"]

        if address == "":
            address = user["address"]

        if latin_honors == "":
            latin_honors = user["latin_honors"]

        if email == "":
            email = user["email"]

        if course == "":
            course = user["course"]

        if graduation_year == "":
            graduation_year = user["graduation_year"]

        # Duplicate Username

        if self.user_model.username_exists(
            username,
            user["id"]
        ):

            self.toast_error("Username already exists.", "Duplicate Username")

            return

        # Duplicate Student Number

        if self.user_model.student_number_exists(
            student_number,
            user["id"]
        ):

            self.toast_error("Student number already exists.", "Duplicate Student Number")

            return

        # Update Database

        self.user_model.update_profile(

            user["id"],

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
            latin_honors

        )

        # Refresh Session

        updated_user = self.user_model.get_user_by_id(
            user["id"]
        )

        login(updated_user)

        self.toast_success("Profile updated successfully!")

        self.cancel_edit()
    
    def change_profile_picture(self):

        filename = filedialog.askopenfilename(

            title="Choose Profile Picture",

            filetypes=[
                ("Image Files","*.png *.jpg *.jpeg")
            ]
        )

        if not filename:
            return

        pictures_dir = resolve_asset_path("profile_pictures")

        os.makedirs(
            pictures_dir,
            exist_ok=True
        )

        extension = os.path.splitext(filename)[1]

        relative_destination = os.path.join(
            "profile_pictures",
            f"user_{get_user()['id']}{extension}"
        )

        destination = resolve_asset_path(relative_destination)

        shutil.copy(filename, destination)

        self.user_model.update_profile_picture(

            get_user()["id"],

            relative_destination
        )

        updated_user = self.user_model.get_user_by_id(
            get_user()["id"]
        )

        login(updated_user)

        self.load_profile_picture()

    def remove_profile_picture(self):

        user = get_user()

        if not user:
            return

        self.user_model.update_profile_picture(
            user["id"],
            ""
        )

        updated_user = self.user_model.get_user_by_id(
            user["id"]
        )

        login(updated_user)

        self.load_profile_picture()

        self.toast_success("Profile picture removed.")

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