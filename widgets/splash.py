# ==========================================
# DLSAU Alumni Tracking System
# widgets/splash.py
# ==========================================
#
# A branded loading screen shown once, on the very first run of the
# app, before the main window is revealed.

import os
import tkinter as tk

import theme

try:
    from PIL import Image, ImageTk
    _PIL_OK = True
except ImportError:
    _PIL_OK = False


class SplashScreen(tk.Toplevel):

    def __init__(self, root, logo_path, on_done, duration=2200):

        super().__init__(root)

        self.root = root
        self.on_done = on_done
        self.duration = duration

        self.overrideredirect(True)
        self.configure(bg=theme.PRIMARY)
        self.attributes("-topmost", True)

        # Center on screen
        w, h = 640, 420
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        wrapper = tk.Frame(self, bg=theme.PRIMARY)
        wrapper.pack(fill="both", expand=True)

        spacer_top = tk.Frame(wrapper, bg=theme.PRIMARY)
        spacer_top.pack(expand=True, fill="both")

        # Logo
        self._logo_img = None
        if os.path.exists(logo_path) and _PIL_OK:
            try:
                img = Image.open(logo_path)
                img.thumbnail((140, 140))
                self._logo_img = ImageTk.PhotoImage(img)
            except Exception:
                self._logo_img = None

        if self._logo_img is not None:
            tk.Label(
                wrapper, image=self._logo_img, bg=theme.PRIMARY
            ).pack(pady=(0, 18))

        tk.Label(
            wrapper,
            text="DLSAU ALUMNI TRACKING SYSTEM",
            font=(theme.TITLE_FONT_NAME, 22, "bold"),
            bg=theme.PRIMARY,
            fg=theme.WHITE,
        ).pack()

        tk.Label(
            wrapper,
            text="Connecting Alumni for Success and Transformation",
            font=(theme.BODY_FONT_NAME, 12),
            bg=theme.PRIMARY,
            fg=theme.PRIMARY_TINT,
        ).pack(pady=(6, 30))

        # Progress bar track
        track = tk.Frame(wrapper, bg=theme.PRIMARY_LIGHT, width=360, height=8)
        track.pack()
        track.pack_propagate(False)

        self.bar = tk.Frame(track, bg=theme.WHITE, width=0, height=8)
        self.bar.place(x=0, y=0, relheight=1)

        self.status = tk.Label(
            wrapper,
            text="Loading system components...",
            font=(theme.BODY_FONT_NAME, 10),
            bg=theme.PRIMARY,
            fg=theme.PRIMARY_TINT,
        )
        self.status.pack(pady=(14, 0))

        spacer_bottom = tk.Frame(wrapper, bg=theme.PRIMARY)
        spacer_bottom.pack(expand=True, fill="both")

        tk.Label(
            wrapper,
            text="\u00a9 De La Salle Araneta University",
            font=(theme.BODY_FONT_NAME, 9),
            bg=theme.PRIMARY,
            fg=theme.PRIMARY_TINT,
        ).pack(pady=(0, 14))

        self.track_width = 360
        self._progress = 0
        self._messages = [
            "Loading system components...",
            "Preparing alumni database...",
            "Setting up your workspace...",
            "Almost ready...",
        ]

        self._animate()

    def _animate(self):
        step_time = max(self.duration // 100, 10)
        self._progress += 1
        pct = self._progress / 100
        self.bar.configure(width=int(self.track_width * pct))

        msg_index = min(int(pct * len(self._messages)), len(self._messages) - 1)
        self.status.configure(text=self._messages[msg_index])

        if self._progress < 100:
            self.after(step_time, self._animate)
        else:
            self.after(150, self._finish)

    def _finish(self):
        try:
            self.destroy()
        except tk.TclError:
            pass
        if self.on_done:
            self.on_done()
