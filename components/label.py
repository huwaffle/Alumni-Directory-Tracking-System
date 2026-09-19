# ==========================================
# DLSAU Alumni Tracking System
# components/label.py
# ==========================================

import tkinter as tk

import theme


class PrimaryLabel(tk.Label):

    def __init__(self, parent, text, bg=None):

        super().__init__(
            parent,
            text=text,
            font=theme.FONT_LABEL,
            bg=bg or theme.BG_COLOR,
            fg=theme.TEXT_PRIMARY,
            anchor="e",
        )
