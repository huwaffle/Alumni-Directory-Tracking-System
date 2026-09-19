# ==========================================
# DLSAU Alumni Tracking System
# widgets/confirm_dialog.py
# ==========================================
#
# A branded confirmation dialog that replaces tkinter's default
# messagebox.askyesno popups (which look like bare OS dialogs and
# clash with the rest of the app). Used anywhere a destructive or
# important action needs a yes/no confirmation — most notably when
# deleting an alumni record.
#
# Usage:
#   from widgets.confirm_dialog import ConfirmDialog
#
#   if ConfirmDialog.ask(
#       self,
#       title="Delete Alumni",
#       message="Are you sure you want to delete this alumni record?",
#       detail="This action cannot be undone.",
#       confirm_text="Delete",
#       danger=True,
#   ):
#       ...

import tkinter as tk

import theme


class ConfirmDialog(tk.Toplevel):

    ICONS = {
        "danger": "\u26A0",   # warning triangle
        "warning": "\u26A0",
        "info": "\u2139",
    }

    def __init__(
        self,
        parent,
        title="Please Confirm",
        message="Are you sure?",
        detail=None,
        confirm_text="Confirm",
        cancel_text="Cancel",
        danger=False,
    ):

        super().__init__(parent)

        self.result = False
        self._parent = parent

        accent = theme.ERROR if danger else theme.PRIMARY
        icon = self.ICONS["danger" if danger else "info"]

        # -----------------------------
        # Window setup
        # -----------------------------
        self.withdraw()
        self.overrideredirect(True)
        self.configure(bg=theme.BORDER_COLOR)
        self.attributes("-topmost", True)
        try:
            self.attributes("-alpha", 0.0)
        except tk.TclError:
            pass

        # -----------------------------
        # Dimmed overlay behind the dialog, drawn over the parent window,
        # so focus is pulled to the confirmation instead of the page
        # behind it.
        # -----------------------------
        self._overlay = tk.Toplevel(parent)
        self._overlay.overrideredirect(True)
        self._overlay.configure(bg=theme.BLACK)
        try:
            self._overlay.attributes("-alpha", 0.0)
        except tk.TclError:
            pass
        self._overlay.attributes("-topmost", True)

        root = parent.winfo_toplevel()
        rx, ry = root.winfo_rootx(), root.winfo_rooty()
        rw, rh = root.winfo_width(), root.winfo_height()
        self._overlay.geometry(f"{rw}x{rh}+{rx}+{ry}")

        # -----------------------------
        # Card
        # -----------------------------
        card = tk.Frame(self, bg=theme.WHITE)
        card.pack(padx=1, pady=1)

        # accent header strip
        strip = tk.Frame(card, bg=accent, height=6)
        strip.pack(fill="x")

        body = tk.Frame(card, bg=theme.WHITE)
        body.pack(fill="both", expand=True, padx=32, pady=(24, 20))

        icon_circle = tk.Canvas(
            body, width=56, height=56, bg=theme.WHITE, highlightthickness=0
        )
        icon_circle.pack(pady=(0, 14))
        icon_circle.create_oval(2, 2, 54, 54, fill=self._tint(accent), outline="")
        icon_circle.create_text(
            28, 28, text=icon, font=(theme.BODY_FONT_NAME, 22, "bold"), fill=accent
        )

        tk.Label(
            body,
            text=title,
            font=theme.FONT_H2,
            bg=theme.WHITE,
            fg=theme.TEXT_PRIMARY,
            justify="center",
        ).pack()

        tk.Label(
            body,
            text=message,
            font=theme.FONT_BODY,
            bg=theme.WHITE,
            fg=theme.TEXT_SECONDARY,
            justify="center",
            wraplength=340,
        ).pack(pady=(10, 0))

        if detail:
            tk.Label(
                body,
                text=detail,
                font=theme.FONT_SMALL,
                bg=theme.WHITE,
                fg=theme.TEXT_MUTED,
                justify="center",
                wraplength=340,
            ).pack(pady=(6, 0))

        button_row = tk.Frame(body, bg=theme.WHITE)
        button_row.pack(pady=(24, 0))

        cancel_btn = tk.Button(
            button_row,
            text=cancel_text,
            command=self._on_cancel,
            font=theme.FONT_BUTTON,
            bg=theme.WHITE,
            fg=theme.TEXT_SECONDARY,
            activebackground=theme.PRIMARY_TINT,
            activeforeground=theme.TEXT_PRIMARY,
            bd=1,
            highlightbackground=theme.BORDER_COLOR,
            highlightthickness=1,
            relief="flat",
            width=14,
            height=2,
            cursor="hand2",
        )
        cancel_btn.pack(side="left", padx=(0, 10))

        confirm_btn = tk.Button(
            button_row,
            text=confirm_text,
            command=self._on_confirm,
            font=theme.FONT_BUTTON,
            bg=accent,
            fg=theme.WHITE,
            activebackground=self._darken(accent),
            activeforeground=theme.WHITE,
            bd=0,
            relief="flat",
            width=14,
            height=2,
            cursor="hand2",
        )
        confirm_btn.pack(side="left")

        for btn, base in ((cancel_btn, theme.WHITE), (confirm_btn, accent)):
            hover = theme.PRIMARY_TINT if base == theme.WHITE else self._darken(base)
            btn.bind("<Enter>", lambda e, b=btn, h=hover: b.configure(bg=h))
            btn.bind("<Leave>", lambda e, b=btn, base=base: b.configure(bg=base))

        self.bind("<Escape>", lambda e: self._on_cancel())
        self.bind("<Return>", lambda e: self._on_confirm())

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

        self.update_idletasks()
        self._center_over(root)

        self._fade_in()
        confirm_btn.focus_set()

        self.transient(root)
        self.grab_set()
        self.wait_window(self)

    # -----------------------------------------
    @staticmethod
    def _tint(hex_color, amount=0.85):
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        r = int(r + (255 - r) * amount)
        g = int(g + (255 - g) * amount)
        b = int(b + (255 - b) * amount)
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def _darken(hex_color, amount=0.18):
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        r = int(r * (1 - amount))
        g = int(g * (1 - amount))
        b = int(b * (1 - amount))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _center_over(self, root):
        w = max(self.winfo_reqwidth(), 420)
        h = self.winfo_reqheight()
        rx, ry = root.winfo_rootx(), root.winfo_rooty()
        rw, rh = root.winfo_width(), root.winfo_height()
        x = rx + (rw - w) // 2
        y = ry + (rh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _fade_in(self, alpha=0.0):
        try:
            alpha = min(alpha + 0.2, 1.0)
            self._overlay.attributes("-alpha", alpha * 0.35)
            self.attributes("-alpha", alpha)
            if alpha < 1.0:
                self.deiconify()
                self.after(12, lambda: self._fade_in(alpha))
            else:
                self.deiconify()
                self.lift()
        except tk.TclError:
            pass

    def _on_confirm(self):
        self.result = True
        self._close()

    def _on_cancel(self):
        self.result = False
        self._close()

    def _close(self):
        try:
            self._overlay.destroy()
        except tk.TclError:
            pass
        try:
            self.grab_release()
            self.destroy()
        except tk.TclError:
            pass

    @classmethod
    def ask(
        cls,
        parent,
        title="Please Confirm",
        message="Are you sure?",
        detail=None,
        confirm_text="Confirm",
        cancel_text="Cancel",
        danger=False,
    ):
        dialog = cls(
            parent,
            title=title,
            message=message,
            detail=detail,
            confirm_text=confirm_text,
            cancel_text=cancel_text,
            danger=danger,
        )
        return dialog.result
