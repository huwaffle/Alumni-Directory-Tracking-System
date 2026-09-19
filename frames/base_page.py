# ==========================================
# frames/base_page.py
# ==========================================

import tkinter as tk
import os

from PIL import Image, ImageTk

import theme
from widgets import toast
from config import BASE_DIR


class BasePage(tk.Frame):

    BG_COLOR = theme.BG_COLOR
    TITLE_FONT = theme.FONT_H1

    def __init__(self, parent, controller):

        super().__init__(parent, bg=self.BG_COLOR)

        self.controller = controller

        # ==========================================
        # Background Image
        # ==========================================

        bg_path = os.path.join(BASE_DIR, "assets", "background.png")

        if os.path.exists(bg_path):
            self._bg_original = Image.open(bg_path)
        else:
            self._bg_original = None

        self._bg_label = tk.Label(
            self,
            bd=0
        )

        self._bg_label.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        self.bind(
            "<Configure>",
            self._resize_background
        )

    def create_title(self, text, parent=None):

        return tk.Label(
            parent if parent is not None else self,
            text=text,
            font=self.TITLE_FONT,
            bg=self.BG_COLOR,
            fg=theme.PRIMARY,
            justify="center",
        )

    # -----------------------------------------------------
    # Framed content pane
    # -----------------------------------------------------
    # Every page sits on top of the full-bleed background image. Rather
    # than letting page content cover the entire window edge-to-edge
    # (which hides the background completely), pages should build their
    # UI inside the frame returned here: a centered pane inset from the
    # window edges so the background photo shows through as a soft
    # border/frame around every screen. This is the single shared
    # mechanism that keeps every page centered and visually consistent.
    # -----------------------------------------------------

    def create_content_pane(self, inset=0.045):

        pane = tk.Frame(self, bg=self.BG_COLOR)

        pane.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            relwidth=1 - (inset * 2),
            relheight=1 - (inset * 2),
        )

        return pane

    # -----------------------------------------------------
    # Scrollable framed content pane
    # -----------------------------------------------------
    # Same idea as create_content_pane(), but for pages whose content is
    # taller than the window and needs to scroll. Sets up self.canvas /
    # self.content / self.canvas_window exactly like before, just inset
    # from the window edges. Subclasses are expected to define
    # resize_content(event), bind_mousewheel(event) and
    # unbind_mousewheel(event) as before.
    # -----------------------------------------------------

    def setup_scrollable_content(self, inset=0.045):

        shell = self.create_content_pane(inset=inset)

        self.canvas = tk.Canvas(
            shell,
            bg=self.BG_COLOR,
            highlightthickness=0,
        )

        scrollbar = tk.Scrollbar(
            shell,
            orient="vertical",
            command=self.canvas.yview,
        )

        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")

        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.focus_set()

        self.content = tk.Frame(self.canvas, bg=self.BG_COLOR)

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="n",
        )

        self.content.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )

        self.canvas.bind("<Configure>", self.resize_content)
        self.content.bind("<Enter>", self.bind_mousewheel)
        self.content.bind("<Leave>", self.unbind_mousewheel)

        return self.content

    # -----------------------------------------------------
    # Scrollable content area
    # -----------------------------------------------------
    # Every page can call self.make_scrollable() once, then place its
    # content inside the returned frame instead of `self` directly.
    # This keeps everything large & scrollable for presentations on
    # smaller screens/projectors.
    # -----------------------------------------------------

    def make_scrollable(self, bg=None):

        bg = bg or self.BG_COLOR

        outer = tk.Frame(self, bg=bg)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            outer,
            bg=bg,
            highlightthickness=0,
            bd=0,
        )
        vscroll = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        inner = tk.Frame(canvas, bg=bg)
        window_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_inner_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_canvas_configure(event):
            # stretch the inner frame to the full canvas width so that
            # anything centered inside it (via pack's default center
            # anchor) is centered on screen, not on its own content size
            canvas.itemconfig(window_id, width=event.width)

        inner.bind("<Configure>", _on_inner_configure)
        canvas.bind("<Configure>", _on_canvas_configure)

        def _on_mousewheel(event):
            if event.num == 4:
                delta = -1
            elif event.num == 5:
                delta = 1
            else:
                delta = -1 * int(event.delta / 120)
            canvas.yview_scroll(delta, "units")

        def _bind_wheel(_):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            canvas.bind_all("<Button-4>", _on_mousewheel)
            canvas.bind_all("<Button-5>", _on_mousewheel)

        def _unbind_wheel(_):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        canvas.bind("<Enter>", _bind_wheel)
        canvas.bind("<Leave>", _unbind_wheel)

        self._canvas = canvas
        self._scroll_inner = inner

        return inner

    # -----------------------------------------------------
    # Toast helpers (replaces tkinter.messagebox everywhere)
    # -----------------------------------------------------

    def toast_success(self, message, title="Success"):
        toast.success(self, message, title)

    def toast_error(self, message, title="Error"):
        toast.error(self, message, title)

    def toast_warning(self, message, title="Warning"):
        toast.warning(self, message, title)

    def toast_info(self, message, title="Notice"):
        toast.info(self, message, title)

    def _resize_background(self, event):

        if self._bg_original is None:
            return

        image = self._bg_original.resize(
            (event.width, event.height),
            Image.LANCZOS
        )

        self._bg_photo = ImageTk.PhotoImage(image)

        self._bg_label.configure(
            image=self._bg_photo
        )

        self._bg_label.lower()
