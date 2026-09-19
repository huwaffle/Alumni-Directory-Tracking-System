# ==========================================
# DLSAU Alumni Tracking System
# theme.py — Centralized Design System
# ==========================================
#
# Brand palette:  Pantone 627C (deep teal-green), White, True Black
# Typography:     PT Serif for titles/headings, Helvetica for body text
#
# Everything visual in the app should pull from this file so the whole
# system stays consistent and can be re-themed from a single place.

import tkinter as tk
import tkinter.font as tkfont

# -----------------------------------------
# COLORS
# -----------------------------------------

PANTONE_627C = "#13322B"      # primary brand color
PRIMARY = PANTONE_627C
PRIMARY_DARK = "#0B1F1A"      # pressed / hover-dark state
PRIMARY_LIGHT = "#1E4A40"     # hover state (lighter than primary)
PRIMARY_TINT = "#E7EDEB"      # very light tint of primary, for subtle backgrounds
PRIMARY_TINT_2 = "#D2DEDA"    # slightly stronger tint, for borders/dividers

WHITE = "#FFFFFF"
BLACK = "#000000"             # true black, used sparingly (body text, accents)

BG_COLOR = "#F4F6F5"          # app background (near-white, warms up pure white)
CARD_COLOR = WHITE
BORDER_COLOR = "#D6DEDC"

TEXT_PRIMARY = BLACK
TEXT_SECONDARY = "#3F4947"
TEXT_ON_PRIMARY = WHITE
TEXT_MUTED = "#6B7573"

SUCCESS = "#1E7A46"
ERROR = "#B3261E"
WARNING = "#B7791E"
INFO = PANTONE_627C

# -----------------------------------------
# TYPOGRAPHY
# -----------------------------------------

TITLE_FONT_NAME = "PT Serif"
BODY_FONT_NAME = "Helvetica"

# Font tuples: (family, size, weight)
FONT_DISPLAY = (TITLE_FONT_NAME, 34, "bold")     # hero / splash titles
FONT_H1 = (TITLE_FONT_NAME, 26, "bold")          # page titles
FONT_H2 = (TITLE_FONT_NAME, 20, "bold")          # section / card titles
FONT_H3 = (TITLE_FONT_NAME, 16, "bold")          # sub-section titles

FONT_BODY_LG = (BODY_FONT_NAME, 14)
FONT_BODY = (BODY_FONT_NAME, 13)
FONT_BODY_BOLD = (BODY_FONT_NAME, 13, "bold")
FONT_LABEL = (BODY_FONT_NAME, 12, "bold")
FONT_SMALL = (BODY_FONT_NAME, 11)
FONT_BUTTON = (BODY_FONT_NAME, 13, "bold")
FONT_TABLE_HEADER = (BODY_FONT_NAME, 12, "bold")
FONT_TABLE_ROW = (BODY_FONT_NAME, 11)

_FONTS_READY = False


def init_fonts(root=None):
    """Register/normalize the named fonts once a Tk root exists.
    Falls back gracefully if PT Serif isn't installed on the machine."""
    global _FONTS_READY, TITLE_FONT_NAME

    if _FONTS_READY:
        return

    try:
        available = set(tkfont.families(root))
    except Exception:
        available = set()

    if "PT Serif" not in available:
        # Graceful fallback chain so the UI never breaks if the font
        # isn't installed on the presenting machine.
        for fallback in ("Georgia", "Times New Roman", "Times", "serif"):
            if fallback in available:
                TITLE_FONT_NAME = fallback
                break

    _refresh_font_tuples()
    _FONTS_READY = True


def _refresh_font_tuples():
    global FONT_DISPLAY, FONT_H1, FONT_H2, FONT_H3
    FONT_DISPLAY = (TITLE_FONT_NAME, 34, "bold")
    FONT_H1 = (TITLE_FONT_NAME, 26, "bold")
    FONT_H2 = (TITLE_FONT_NAME, 20, "bold")
    FONT_H3 = (TITLE_FONT_NAME, 16, "bold")


# -----------------------------------------
# SPACING / SIZING (kept large per presentation requirements)
# -----------------------------------------

PAD_SM = 8
PAD_MD = 16
PAD_LG = 28
PAD_XL = 40

BUTTON_WIDTH = 26
BUTTON_HEIGHT = 2
ENTRY_WIDTH = 34

RADIUS = 10  # used by canvas-drawn rounded elements
