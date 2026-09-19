# ==========================================
# DLSAU Alumni Tracking System
# frames/register.py
# ==========================================

import tkinter as tk

from auth import Auth

from frames.base_page import BasePage

from components.button import PrimaryButton
from components.entry import PrimaryEntry
from components.label import PrimaryLabel
from components.combobox import PrimaryCombobox

from tkinter import filedialog
import shutil
import os

from config import resolve_asset_path

class RegisterPage(BasePage):

    def __init__(self, parent, controller):

        super().__init__(parent, controller)

        # ==========================================
        # Scrollable Canvas
        # ==========================================

        self.content = self.setup_scrollable_content()

        self.auth = Auth()

        self.profile_picture = "assets/default.png"

        # ==========================================
        # Form Frame
        # ==========================================

        self.form_frame = tk.Frame(
            self.content,
            bg=self.BG_COLOR
        )

        self.form_frame.pack(pady=20)

        self.table = tk.Frame(
            self.form_frame,
            bg="white",
            bd=1,
            relief="solid"
        )


        tk.Label(
            self.form_frame,
            text="Alumni Registration",
            bg=self.BG_COLOR,
            font=("Helvetica", 26, "bold")
        ).pack(
            pady=(20, 10)
        )

        self.table.pack(
            pady=15,
            padx=20
        )

        self.table.grid_columnconfigure(
            0,
            weight=0
        )

        self.table.grid_columnconfigure(
            1,
            weight=1
        )

        self.inputs = {}

        self.fields = [

            ("PERSONAL INFORMATION", None),

            ("Student Number", "student_number"),
            ("First Name", "first_name"),
            ("Middle Name", "middle_name"),
            ("Last Name", "last_name"),
            ("Sex", "sex"),
            ("Age", "age"),
            ("Civil Status", "civil_status"),
            ("Address", "address"),
            ("Email", "email"),
            ("Profile Picture", "profile_picture"),

            ("ACADEMIC INFORMATION", None),

            ("Course", "course"),
            ("Graduation Year", "graduation_year"),
            ("Latin Honors", "latin_honors"),

            ("ACCOUNT INFORMATION", None),

            ("Username", "username"),
            ("Password", "password"),
            ("Confirm Password", "confirm_password")
        ]

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
            # Left Column
            # -----------------------------
            label_frame = tk.Frame(
                self.table,
                bg="#D6DEDC"
            )

            label_frame.grid(
                row=row,
                column=0,
                sticky="nsew"
            )

            tk.Label(
                label_frame,
                text=title,
                bg="#D6DEDC",
                font=("Helvetica", 14, "bold"),
                anchor="w"
            ).pack(
                side="left",
                padx=(10, 0),
                pady=10
            )

            # Every field is required
            tk.Label(
                label_frame,
                text=" *",
                fg="red",
                bg="#D6DEDC",
                font=("Helvetica", 14, "bold")
            ).pack(
                side="left",
                pady=10
            )

            # -----------------------------
            # Right Column
            # -----------------------------

            if key == "sex":

                widget = PrimaryCombobox(
                    self.table,
                    [
                        "Male",
                        "Female"
                    ]
                )

            elif key == "age":

                widget = PrimaryCombobox(
                    self.table,
                    [
                        "Below 21",
                        "21-25",
                        "26-30",
                        "Above 35"
                    ]
                )

            elif key == "civil_status":

                widget = PrimaryCombobox(
                    self.table,
                    [
                        "Single",
                        "Married",
                        "Widowed",
                        "Prefer not to say"
                    ]
                )

            elif key == "course":

                widget = PrimaryCombobox(
                    self.table,
                    [
                        "BSCS",
                        "BSCoE",
                        "ABPsych"
                    ]
                )

            elif key == "graduation_year":

                years = [str(year) for year in range(2026, 1989, -1)]

                widget = PrimaryCombobox(
                    self.table,
                    years
                )

            elif key == "latin_honors":

                widget = PrimaryCombobox(
                    self.table,
                    [
                        "Summa Cum Laude",
                        "Magna Cum Laude",
                        "Cum Laude",
                        "None"
                    ]
                )
            
            elif key == "profile_picture":

                frame = tk.Frame(
                    self.table,
                    bg="white"
                )

                button = PrimaryButton(
                    frame,
                    "Choose Image",
                    self.browse_picture
                )

                button.pack(
                    side="left"
                )

                self.picture_label = tk.Label(
                    frame,
                    text="No file selected",
                    bg="white",
                    anchor="w"
                )

                self.picture_label.pack(
                    side="left",
                    padx=10
                )

                widget = frame

            elif key == "address":

                widget = tk.Text(
                    self.table,
                    width=30,
                    height=3,
                    font=("Helvetica", 14)
                )

            elif key == "password":

                widget = PrimaryEntry(
                    self.table,
                    show="*"
                )

            elif key == "confirm_password":

                widget = PrimaryEntry(
                    self.table,
                    show="*"
                )

            else:

                widget = PrimaryEntry(self.table)

            widget.grid(
                row=row,
                column=1,
                sticky="ew",
                padx=8,
                pady=6
            )

            self.inputs[key] = widget

            setattr(self, key, widget)

            row += 1

        # ==========================
        # Buttons
        # ==========================

        PrimaryButton(
            self.form_frame,
            "Register",
            self.register
        ).pack(
            pady=(20, 10)
        )

        PrimaryButton(
            self.form_frame,
            text="Back",
            command=lambda: controller.show_frame("WelcomePage")
        ).pack(
            pady=(0, 20)
        )

    # ======================================

    def register(self):

        # --------------------------------------
        # Check for missing required fields
        # --------------------------------------

        required_fields = {

            "Student Number": self.student_number.get().strip(),
            "First Name": self.first_name.get().strip(),
            "Last Name": self.last_name.get().strip(),
            "Sex": self.sex.get().strip(),
            "Age": self.age.get().strip(),
            "Civil Status": self.civil_status.get().strip(),
            "Address": self.address.get("1.0", "end-1c").strip(),
            "Email": self.email.get().strip(),
            "Course": self.course.get().strip(),
            "Graduation Year": self.graduation_year.get().strip(),
            "Latin Honors": self.latin_honors.get().strip(),
            "Username": self.username.get().strip(),
            "Password": self.password.get(),
            "Confirm Password": self.confirm_password.get()

        }

        missing_fields = [

            field

            for field, value in required_fields.items()

            if value == ""

        ]

        if missing_fields:

            self.toast_warning(

                "Please complete all required fields.",

                "Incomplete Form"

            )

            return

        # --------------------------------------
        # Save Profile Picture
        # --------------------------------------

        picture_path = "assets/default.png"

        if self.profile_picture != "assets/default.png":

            extension = os.path.splitext(
                self.profile_picture
            )[1]

            filename = (
                self.student_number.get()
                + extension
            )

            relative_destination = os.path.join(
                "assets",
                "profile_pictures",
                filename
            )

            destination = resolve_asset_path(relative_destination)

            os.makedirs(
                os.path.dirname(destination),
                exist_ok=True
            )

            shutil.copy(
                self.profile_picture,
                destination
            )

            picture_path = relative_destination

        success, message = self.auth.register(

            self.student_number.get(),

            self.username.get(),

            self.password.get(),

            self.confirm_password.get(),

            self.first_name.get(),

            self.middle_name.get(),

            self.last_name.get(),

            self.sex.get(),

            self.age.get(),

            self.civil_status.get(),

            self.email.get(),

            self.address.get("1.0", "end-1c"),

            self.course.get(),

            self.graduation_year.get(),

            self.latin_honors.get(),

            picture_path

        )

        if success:

            self.toast_success(message)

            self.clear_form()

            self.controller.show_frame(
                "WelcomePage"
            )

        else:

            self.toast_error(message, "Registration Failed")

    # ======================================

    def clear_form(self):

        self.student_number.clear()

        self.first_name.clear()

        self.middle_name.clear()

        self.last_name.clear()

        self.sex.clear()

        self.age.clear()

        self.civil_status.clear()

        self.address.delete("1.0", tk.END)

        self.latin_honors.clear()

        self.email.clear()

        self.course.clear()

        self.graduation_year.clear()

        self.username.clear()

        self.password.clear()

        self.confirm_password.clear()
    
    def browse_picture(self):

        filename = filedialog.askopenfilename(

            title="Select Profile Picture",

            filetypes=[

                ("Image Files", "*.png *.jpg *.jpeg")

            ]

        )

        if filename:

            self.profile_picture = filename

            self.picture_label.config(
                text=os.path.basename(filename)
            )
    
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
