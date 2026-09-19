# ==========================================
# DLSAU Alumni Tracking System
# frames/welcome.py
# ==========================================

import os
import tkinter as tk

from frames.base_page import BasePage
from components.button import PrimaryButton, SecondaryButton
import theme
from config import BASE_DIR

try:
    from PIL import Image, ImageTk
    _PIL_OK = True
except ImportError:
    _PIL_OK = False

LOGO_PATH = os.path.join(BASE_DIR, "assets", "developers", "dlsau_logo.png")


class WelcomePage(BasePage):

    def __init__(self, parent, controller):

        super().__init__(parent, controller)

        # ==========================
        # Center Container
        # ==========================
        # (Background image is already drawn by BasePage; this page just
        # needs to sit on top of it, centered, in a clean card so the
        # photo shows through around the edges.)

        container = tk.Frame(self, bg=self.BG_COLOR)
        container.place(relx=0.5, rely=0.5, anchor="center")

        card = tk.Frame(
            container,
            bg=theme.WHITE,
            bd=1,
            relief="solid",
            highlightbackground=theme.BORDER_COLOR,
        )
        card.pack()

        content = tk.Frame(card, bg=theme.WHITE)
        content.pack(padx=56, pady=44)

        # -----------------------------
        # Logo
        # -----------------------------

        self._logo_img = None
        if os.path.exists(LOGO_PATH) and _PIL_OK:
            try:
                img = Image.open(LOGO_PATH)
                img.thumbnail((150, 150))
                self._logo_img = ImageTk.PhotoImage(img)
            except Exception:
                self._logo_img = None

        if self._logo_img is not None:
            tk.Label(
                content,
                image=self._logo_img,
                bg=theme.WHITE,
            ).pack(pady=(0, 20))

        # -----------------------------
        # Title
        # -----------------------------

        tk.Label(
            content,
            text="CAST",
            font=theme.FONT_DISPLAY,
            bg=theme.WHITE,
            fg=theme.PRIMARY,
        ).pack()

        tk.Label(
            content,
            text="CONNECTING ALUMNI FOR SUCCESS AND TRANSFORMATION",
            font=(theme.BODY_FONT_NAME, 13, "bold"),
            bg=theme.WHITE,
            fg=theme.TEXT_SECONDARY,
        ).pack(pady=(4, 2))

        tk.Label(
            content,
            text="De La Salle Araneta University: Alumni Tracking System",
            font=theme.FONT_H2,
            bg=theme.WHITE,
            fg=theme.TEXT_PRIMARY,
        ).pack(pady=(10, 10))

        # divider
        tk.Frame(
            content, bg=theme.PRIMARY_TINT_2, height=2, width=420
        ).pack(pady=(10, 30))

        # -----------------------------
        # Subtitle
        # -----------------------------

        tk.Label(
            content,
            text="Welcome to the Alumni Portal",
            font=theme.FONT_BODY_LG,
            bg=theme.WHITE,
            fg=theme.TEXT_MUTED,
        ).pack(pady=(0, 40))

        # -----------------------------
        # Buttons
        # -----------------------------

        button_col = tk.Frame(content, bg=theme.WHITE)
        button_col.pack()

        PrimaryButton(
            button_col,
            text="Admin Login",
            command=lambda: controller.show_frame("AdminLoginPage")
        ).pack(pady=8)

        PrimaryButton(
            button_col,
            text="Alumni Login",
            command=lambda: controller.show_frame("AlumniLoginPage")
        ).pack(pady=8)

        PrimaryButton(
            button_col,
            text="Alumni Register",
            command=lambda: controller.show_frame("RegisterPage")
        ).pack(pady=8)

        SecondaryButton(
            button_col,
            text="About",
            command=lambda: controller.show_frame("AboutPage")
        ).pack(pady=8)

        SecondaryButton(
            button_col,
            text="Exit",
            command=controller.destroy
        ).pack(pady=8)
