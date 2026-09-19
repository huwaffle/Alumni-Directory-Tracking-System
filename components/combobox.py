# ==========================================
# DLSAU Alumni Tracking System
# components/combobox.py
# ==========================================

from tkinter import ttk

import theme


def _ensure_style():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure(
        "Primary.TCombobox",
        fieldbackground=theme.WHITE,
        background=theme.WHITE,
        foreground=theme.TEXT_PRIMARY,
        arrowcolor=theme.PRIMARY,
        bordercolor=theme.BORDER_COLOR,
        lightcolor=theme.WHITE,
        darkcolor=theme.WHITE,
        padding=6,
    )
    style.map(
        "Primary.TCombobox",
        fieldbackground=[("readonly", theme.WHITE)],
        bordercolor=[("focus", theme.PRIMARY)],
    )


class PrimaryCombobox(ttk.Combobox):

    def __init__(self, parent, values, width=None):

        _ensure_style()

        super().__init__(
            parent,
            values=values,
            state="readonly",
            width=width or (theme.ENTRY_WIDTH - 2),
            font=theme.FONT_BODY_LG,
            style="Primary.TCombobox",
        )

    def clear(self):
        self.set("")
