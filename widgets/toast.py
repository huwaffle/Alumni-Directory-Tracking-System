# ==========================================
# DLSAU Alumni Tracking System
# widgets/toast.py
# ==========================================
#
# A lightweight toast-notification system that replaces tkinter's
# blocking `messagebox` popups. Toasts slide in from the top-right
# corner of the window, auto-dismiss after a few seconds, and can be
# dismissed early by clicking them. Multiple toasts stack vertically.

import tkinter as tk

import theme


class Toast(tk.Toplevel):

    _active = []  # currently displayed toasts (for stacking)

    ICONS = {
        "success": "\u2713",   # check mark
        "error": "\u2715",     # x mark
        "warning": "\u26A0",   # warning triangle
        "info": "\u2139",      # info
    }

    COLORS = {
        "success": theme.SUCCESS,
        "error": theme.ERROR,
        "warning": theme.WARNING,
        "info": theme.INFO,
    }

    def __init__(self, root, title, message, kind="info", duration=3500):

        super().__init__(root)

        self.root = root
        self.duration = duration

        accent = self.COLORS.get(kind, theme.INFO)
        icon = self.ICONS.get(kind, self.ICONS["info"])

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        try:
            self.attributes("-alpha", 0.0)
        except tk.TclError:
            pass
        self.configure(bg=accent)

        outer = tk.Frame(self, bg=accent)
        outer.pack(fill="both", expand=True)

        card = tk.Frame(outer, bg=theme.WHITE)
        card.pack(fill="both", expand=True, padx=(0, 0), pady=0)

        # left accent strip
        strip = tk.Frame(card, bg=accent, width=6)
        strip.pack(side="left", fill="y")

        body = tk.Frame(card, bg=theme.WHITE)
        body.pack(side="left", fill="both", expand=True, padx=(14, 18), pady=14)

        header_row = tk.Frame(body, bg=theme.WHITE)
        header_row.pack(fill="x", anchor="w")

        tk.Label(
            header_row,
            text=icon,
            font=(theme.BODY_FONT_NAME, 14, "bold"),
            bg=theme.WHITE,
            fg=accent,
        ).pack(side="left", padx=(0, 8))

        tk.Label(
            header_row,
            text=title,
            font=theme.FONT_BODY_BOLD,
            bg=theme.WHITE,
            fg=theme.TEXT_PRIMARY,
            anchor="w",
        ).pack(side="left")

        tk.Label(
            body,
            text=message,
            font=theme.FONT_SMALL,
            bg=theme.WHITE,
            fg=theme.TEXT_SECONDARY,
            anchor="w",
            justify="left",
            wraplength=320,
        ).pack(fill="x", pady=(4, 0), anchor="w")

        for widget in (card, body, header_row, strip, outer):
            widget.bind("<Button-1>", lambda e: self._dismiss())

        self.update_idletasks()

        self._position()
        Toast._active.append(self)
        self._reflow()

        self._fade_in()
        self.after(self.duration, self._fade_out)

    # -----------------------------------------
    def _position(self):
        self.root.update_idletasks()
        w = 360
        h = self.winfo_reqheight()
        rx = self.root.winfo_rootx()
        ry = self.root.winfo_rooty()
        rw = self.root.winfo_width()
        x = rx + rw - w - 24
        y = ry + 24
        self.geometry(f"{w}x{h}+{x}+{y}")
        self._height = h

    def _reflow(self):
        """Stack active toasts vertically, most recent on top."""
        y_offset = 24
        rx = self.root.winfo_rootx()
        ry = self.root.winfo_rooty()
        rw = self.root.winfo_width()
        for t in Toast._active:
            if not t.winfo_exists():
                continue
            w = 360
            h = getattr(t, "_height", t.winfo_reqheight())
            x = rx + rw - w - 24
            t.geometry(f"{w}x{h}+{x}+{ry + y_offset}")
            y_offset += h + 12

    def _fade_in(self, alpha=0.0):
        try:
            alpha = min(alpha + 0.15, 1.0)
            self.attributes("-alpha", alpha)
            if alpha < 1.0:
                self.after(15, lambda: self._fade_in(alpha))
        except tk.TclError:
            pass

    def _fade_out(self, alpha=1.0):
        try:
            alpha = max(alpha - 0.15, 0.0)
            self.attributes("-alpha", alpha)
            if alpha > 0.0:
                self.after(15, lambda: self._fade_out(alpha))
            else:
                self._dismiss()
        except tk.TclError:
            self._dismiss()

    def _dismiss(self):
        if self in Toast._active:
            Toast._active.remove(self)
        try:
            self.destroy()
        except tk.TclError:
            pass
        self._reflow_survivors()

    def _reflow_survivors(self):
        y_offset = 24
        for t in list(Toast._active):
            if not t.winfo_exists():
                continue
            try:
                rx = t.root.winfo_rootx()
                ry = t.root.winfo_rooty()
                rw = t.root.winfo_width()
                w = 360
                h = getattr(t, "_height", t.winfo_reqheight())
                x = rx + rw - w - 24
                t.geometry(f"{w}x{h}+{x}+{ry + y_offset}")
                y_offset += h + 12
            except tk.TclError:
                continue


def _show(root_widget, title, message, kind, duration=3500):
    root = root_widget.winfo_toplevel()
    return Toast(root, title, message, kind=kind, duration=duration)


def success(widget, message, title="Success"):
    return _show(widget, title, message, "success")


def error(widget, message, title="Error"):
    return _show(widget, title, message, "error", duration=4500)


def warning(widget, message, title="Warning"):
    return _show(widget, title, message, "warning", duration=4000)


def info(widget, message, title="Notice"):
    return _show(widget, title, message, "info")
