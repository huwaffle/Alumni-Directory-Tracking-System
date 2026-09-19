# ==========================================
# DLSAU Alumni Tracking System
# components/button.py
# ==========================================

import tkinter as tk

import theme


class PrimaryButton(tk.Button):
    """Filled brand-color button with a hover state."""

    def __init__(self, parent, text, command=None, width=None, bg=None, fg=None):

        self._bg = bg or theme.PRIMARY
        self._hover = theme.PRIMARY_LIGHT
        self._fg = fg or theme.TEXT_ON_PRIMARY

        super().__init__(
            parent,
            text=text,
            command=command,
            font=theme.FONT_BUTTON,
            width=width or theme.BUTTON_WIDTH,
            height=theme.BUTTON_HEIGHT,
            bg=self._bg,
            fg=self._fg,
            activebackground=self._hover,
            activeforeground=self._fg,
            bd=0,
            relief="flat",
            cursor="hand2",
        )

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event):
        if self["state"] != "disabled":
            self.configure(bg=self._hover)

    def _on_leave(self, _event):
        if self["state"] != "disabled":
            self.configure(bg=self._bg)


class SecondaryButton(tk.Button):
    """Outlined button — white fill, primary-color border & text."""

    def __init__(self, parent, text, command=None, width=None):

        super().__init__(
            parent,
            text=text,
            command=command,
            font=theme.FONT_BUTTON,
            width=width or theme.BUTTON_WIDTH,
            height=theme.BUTTON_HEIGHT,
            bg=theme.WHITE,
            fg=theme.PRIMARY,
            activebackground=theme.PRIMARY_TINT,
            activeforeground=theme.PRIMARY,
            bd=1,
            highlightbackground=theme.PRIMARY,
            highlightthickness=1,
            relief="flat",
            cursor="hand2",
        )

        self.bind("<Enter>", lambda e: self.configure(bg=theme.PRIMARY_TINT))
        self.bind("<Leave>", lambda e: self.configure(bg=theme.WHITE))


class DangerButton(tk.Button):
    """For destructive actions (delete, reject, etc.)."""

    def __init__(self, parent, text, command=None, width=None):

        super().__init__(
            parent,
            text=text,
            command=command,
            font=theme.FONT_BUTTON,
            width=width or theme.BUTTON_WIDTH,
            height=theme.BUTTON_HEIGHT,
            bg=theme.ERROR,
            fg=theme.WHITE,
            activebackground="#8C1E18",
            activeforeground=theme.WHITE,
            bd=0,
            relief="flat",
            cursor="hand2",
        )

        self.bind("<Enter>", lambda e: self.configure(bg="#8C1E18"))
        self.bind("<Leave>", lambda e: self.configure(bg=theme.ERROR))
