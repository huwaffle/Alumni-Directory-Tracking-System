# ==========================================
# DLSAU Alumni Tracking System
# components/entry.py
# ==========================================

import tkinter as tk

import theme


class PrimaryEntry(tk.Entry):

    def __init__(self, parent, show=None, width=None):

        super().__init__(
            parent,
            font=theme.FONT_BODY_LG,
            width=width or theme.ENTRY_WIDTH,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=theme.BORDER_COLOR,
            highlightcolor=theme.PRIMARY,
            bg=theme.WHITE,
            fg=theme.TEXT_PRIMARY,
            insertbackground=theme.PRIMARY,
            show=show,
        )

    def clear(self):
        self.delete(0, tk.END)
