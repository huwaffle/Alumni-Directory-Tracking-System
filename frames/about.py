import os
import tkinter as tk
from PIL import Image, ImageTk

from frames.base_page import BasePage
from components.button import PrimaryButton
from config import BASE_DIR



class AboutPage(BasePage):

    def __init__(self, parent, controller):

        super().__init__(parent, controller)

        # ==========================================
        # Scrollable Canvas
        # ==========================================

        self.content = self.setup_scrollable_content()

        self.controller = controller

        tk.Label(
            self.content,
            text="About the System",
            font=("Helvetica", 26, "bold"),
            bg=self.BG_COLOR
        ).pack(pady=20)

        description = (
            "The DLSAU Alumni Tracking System is a desktop application\n"
            "developed by BSCS students of De La Salle Araneta University.\n\n"
            "The system allows administrators to manage alumni records,\n"
            "approve registrations, and monitor alumni employment\n"
            "information efficiently."
        )

        tk.Label(
            self.content,
            text=description,
            bg=self.BG_COLOR,
            font=("Helvetica", 14),
            justify="center"
        ).pack(
            pady=(0,30)
        )

        tk.Label(
            self.content,
            text="Development Team",
            font=("Helvetica", 20, "bold"),
            bg=self.BG_COLOR,
            fg="#13322B"
        ).pack(pady=(10,15))

        self.create_member(
            os.path.join(BASE_DIR, "assets", "developers", "alcantara.png"),
            "Carlos S. Alcantara III",
            "Lead Developer & Documentation",
            "Designed and developed the DLSAU Alumni Tracking System, including the user interface, backend logic, database integration, authentication, alumni management, administrator modules, and employment management system."
        )

        self.create_member(
            os.path.join(BASE_DIR, "assets", "developers", "mendoza.png"),
            "Paulo C. Mendoza",
            "Lead Documentation, Assistant Developer, & System Tester",
            "Led project documentation, assisted in developing system, coordinated testing, and ensured overall system quality."
        )

        self.create_member(
            os.path.join(BASE_DIR, "assets", "developers", "zapanta.png"),
            "Marcelino V. Zapanta III",
            "UI Design Consultant, Documentation & System Tester",
            "Designed the graphical user interface and improved the overall user experience."
        )

        tk.Label(
            self.content,
            text=(
                "Version 1.0\n\n"
                "Software Engineering Project\n"
                "De La Salle Araneta University\n\n"
                "© 2026 Group 2 Development Team"
            ),
            bg=self.BG_COLOR,
            justify="center",
            font=("Helvetica", 13)
        ).pack(pady=30)

        PrimaryButton(
            self.content,
            "Back",
            lambda: self.controller.show_frame("WelcomePage")
        ).pack(pady=(0,20))

    def create_member(self, image_path, name, role, description):

        card = tk.Frame(
            self.content,
            bg="white",
            bd=1,
            relief="solid",
            padx=15,
            pady=15,
            width=800      # adjust if needed
        )

        card.pack(
            pady=10,
            anchor="center"
        )

        card.pack_propagate(False)

        card.grid_columnconfigure(
            1,
            weight=1
        )

        # -------------------------
        # Profile Picture
        # -------------------------

        photo = None

        if os.path.exists(image_path):
            try:
                image = Image.open(image_path)
                image = image.resize((110, 110))
                photo = ImageTk.PhotoImage(image)
            except Exception:
                photo = None

        image_label = tk.Label(
            card,
            image=photo,
            text="" if photo else "No Photo",
            bg="white"
        )

        image_label.image = photo

        image_label.grid(
            row=0,
            column=0,
            rowspan=3,
            padx=(0,20)
        )

        # -------------------------
        # Name
        # -------------------------

        tk.Label(
            card,
            text=name,
            bg="white",
            font=("Helvetica", 18, "bold")
        ).grid(
            row=0,
            column=1,
            sticky="w"
        )

        # -------------------------
        # Role
        # -------------------------

        tk.Label(
            card,
            text=role,
            bg="white",
            fg="#13322B",
            font=("Helvetica", 14, "italic")
        ).grid(
            row=1,
            column=1,
            sticky="w",
            pady=(2,8)
        )

        # -------------------------
        # Description
        # -------------------------

        tk.Label(
            card,
            text=description,
            bg="white",
            justify="left",
            wraplength=500,
            width=60,
            anchor="nw"
        ).grid(
            row=2,
            column=1,
            sticky="w"
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