import customtkinter as ctk

from config import *
from cards import create_card
from file_manager import (
    get_files_by_category,
    get_recent_files,
    get_favorite_files,
    upload_file,
    upload_dropped_files,
    get_storage_usage,
)
from utils import format_size

try:
    from tkinterdnd2 import DND_FILES
except ImportError:
    DND_FILES = None


def build_ui(app, dnd_available=False):

    state = {
        "category": "Dashboard",
        "dark_mode": False,
        "resize_job": None,
        "last_columns": None,
    }

    # -----------------------------
    # Window
    # -----------------------------

    app.title(APP_TITLE)
    app.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    app.minsize(1000, 650)
    app.configure(fg_color=APP_BG)

    # =============================
    # Sidebar
    # =============================

    sidebar = ctk.CTkFrame(
        app,
        width=SIDEBAR_WIDTH,
        fg_color=SIDEBAR_BG,
        corner_radius=0
    )

    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    logo = ctk.CTkLabel(
        sidebar,
        text="📂 MY STORAGE",
        font=("Segoe UI", 22, "bold"),
        text_color=TEXT
    )

    logo.pack(pady=(40, 35))

    menu_items = [
        ("🏠", "Dashboard"),
        ("🕒", "Recent"),
        ("⭐", "Favorites"),
        ("📄", "Documents"),
        ("🖼", "Images"),
        ("🎬", "Videos"),
        ("🎵", "Audio"),
        ("📦", "Others"),
    ]

    menu_buttons = {}

    def select_category(category):
        state["category"] = category

        for name, btn in menu_buttons.items():
            btn.configure(fg_color=HOVER if name == category else "transparent")

        load_files()

    for icon, title in menu_items:

        btn = ctk.CTkButton(
            sidebar,
            text=f"{icon}   {title}",
            anchor="w",
            height=MENU_HEIGHT,
            corner_radius=MENU_RADIUS,
            fg_color="transparent",
            hover_color=HOVER,
            text_color=TEXT,
            font=MENU_FONT,
            command=lambda t=title: select_category(t)
        )

        btn.pack(fill="x", padx=18, pady=5)
        menu_buttons[title] = btn

    menu_buttons["Dashboard"].configure(fg_color=HOVER)

    # -----------------------------
    # Storage Usage (bottom of sidebar)
    # -----------------------------

    storage_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    storage_frame.pack(side="bottom", fill="x", padx=18, pady=25)

    storage_label = ctk.CTkLabel(
        storage_frame, text="Storage used",
        font=("Segoe UI", 12), text_color=TEXT_LIGHT
    )
    storage_label.pack(anchor="w")

    storage_bar = ctk.CTkProgressBar(
        storage_frame, height=10, corner_radius=5, progress_color=PRIMARY
    )
    storage_bar.pack(fill="x", pady=(8, 6))
    storage_bar.set(0)

    storage_detail = ctk.CTkLabel(
        storage_frame, text="", font=("Segoe UI", 11), text_color=TEXT_LIGHT
    )
    storage_detail.pack(anchor="w")

    def update_storage_usage():
        used = get_storage_usage()
        limit_bytes = STORAGE_LIMIT_GB * 1024 ** 3
        fraction = min(used / limit_bytes, 1.0) if limit_bytes else 0
        storage_bar.set(fraction)
        storage_detail.configure(text=f"{format_size(used)} of {STORAGE_LIMIT_GB} GB")

    # =============================
    # Workspace
    # =============================

    workspace = ctk.CTkFrame(app, fg_color=APP_BG, corner_radius=0)
    workspace.pack(side="left", fill="both", expand=True)

    # =============================
    # Top Bar
    # =============================

    topbar = ctk.CTkFrame(
        workspace,
        fg_color=TOPBAR_BG,
        height=TOPBAR_HEIGHT,
        corner_radius=20
    )

    topbar.pack(fill="x", padx=25, pady=25)
    topbar.pack_propagate(False)

    search = ctk.CTkEntry(
        topbar,
        width=SEARCH_WIDTH,
        height=SEARCH_HEIGHT,
        corner_radius=20,
        border_width=1,
        border_color=BORDER,
        placeholder_text="Search files..."
    )

    search.pack(side="left", padx=20)

    spacer = ctk.CTkFrame(topbar, fg_color="transparent")
    spacer.pack(side="left", expand=True, fill="x")

    # -----------------------------
    # Dark mode toggle
    # -----------------------------

    def toggle_dark_mode():
        state["dark_mode"] = not state["dark_mode"]
        ctk.set_appearance_mode("dark" if state["dark_mode"] else "light")
        dark_btn.configure(text="☀" if state["dark_mode"] else "🌙")

    dark_btn = ctk.CTkButton(
        topbar,
        text="🌙",
        width=42,
        height=UPLOAD_HEIGHT,
        corner_radius=20,
        fg_color="transparent",
        hover_color=HOVER,
        text_color=TEXT,
        font=("Segoe UI", 16),
        command=toggle_dark_mode
    )

    dark_btn.pack(side="right", padx=(0, 10))

    upload = ctk.CTkButton(
        topbar,
        text="+ Upload",
        width=120,
        height=UPLOAD_HEIGHT,
        corner_radius=20,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        font=BUTTON_FONT
    )

    upload.pack(side="right", padx=(0, 10))

    avatar = ctk.CTkLabel(
        topbar,
        text="👤",
        font=("Segoe UI Emoji", 24)
    )

    avatar.pack(side="right", padx=20)

    # =============================
    # Content
    # =============================

    content = ctk.CTkFrame(workspace, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=25, pady=(0, 25))

    header = ctk.CTkFrame(content, fg_color="transparent")
    header.pack(fill="x")

    header_title = ctk.CTkLabel(
        header, text="Dashboard", font=TITLE_FONT, text_color=TEXT
    )
    header_title.pack(anchor="w")

    count = ctk.CTkLabel(
        header, text="", font=SUBTITLE_FONT, text_color=TEXT_LIGHT
    )
    count.pack(anchor="w", pady=(5, 15))

    # Upload progress bar - packed/unpacked on demand
    progress_bar = ctk.CTkProgressBar(
        content, height=8, corner_radius=4, progress_color=PRIMARY
    )
    progress_bar.set(0)

    if not dnd_available:
        dnd_notice = ctk.CTkLabel(
            content,
            text="Tip: install 'tkinterdnd2' (pip install tkinterdnd2) to enable drag & drop uploads.",
            font=("Segoe UI", 11),
            text_color=TEXT_LIGHT
        )
        dnd_notice.pack(anchor="w", pady=(0, 10))

    file_grid = ctk.CTkScrollableFrame(content, fg_color="transparent")
    file_grid.pack(fill="both", expand=True)

    # =============================
    # Load Files
    # =============================

    def load_files():

        for widget in file_grid.winfo_children():
            widget.destroy()

        query = search.get().lower()
        category = state["category"]

        header_title.configure(text=category)

        if category == "Recent":
            files = get_recent_files()
        elif category == "Favorites":
            files = get_favorite_files()
        else:
            files = get_files_by_category(category, CATEGORY_EXTENSIONS)

        if query:
            files = [f for f in files if query in f.name.lower()]

        count.configure(text=f"{len(files)} Files")

        if not files:
            empty_text = "Drag & drop files here, or use the Upload button" \
                if category == "Dashboard" else "No files here yet."

            ctk.CTkLabel(
                file_grid, text=empty_text,
                font=("Segoe UI", 13), text_color=TEXT_LIGHT
            ).pack(pady=60)

            update_storage_usage()
            return

        # Responsive column count based on the grid's current width,
        # so resizing the window reflows the cards instead of staying
        # locked to a fixed CARDS_PER_ROW.
        columns = compute_columns()
        state["last_columns"] = columns

        for index, file in enumerate(files):
            row = index // columns
            column = index % columns
            create_card(file_grid, file, row, column, load_files)

        update_storage_usage()

    # =============================
    # Responsive re-layout on window resize (debounced)
    # =============================
    #
    # IMPORTANT: this listens on `content` (a stable container that
    # only resizes when the actual window is resized), NOT on
    # `file_grid` itself. file_grid's contents are destroyed and
    # rebuilt every time load_files() runs, which fires its own
    # <Configure> event - binding the listener there would cause an
    # infinite reload loop (cards constantly flashing/blinking).
    #
    # As a second safety net, we only actually reload if the number
    # of columns the new width would produce has changed, so tiny/
    # inconsequential resize events don't trigger a rebuild either.

    def compute_columns():
        available_width = file_grid.winfo_width()
        card_slot = CARD_WIDTH + (GRID_PADDING * 2)
        return max(1, available_width // card_slot) if available_width > 1 else CARDS_PER_ROW

    def maybe_reload_for_resize():
        if compute_columns() != state["last_columns"]:
            load_files()

    def on_resize(event):
        if state["resize_job"]:
            app.after_cancel(state["resize_job"])
        state["resize_job"] = app.after(250, maybe_reload_for_resize)

    content.bind("<Configure>", on_resize)

    # =============================
    # Upload + progress bar handling
    # =============================

    def show_progress():
        # NOTE: we reference `after=header` here, not `before=file_grid`.
        # CTkScrollableFrame is a compound widget - the Python object
        # `file_grid` is actually the *inner* scrollable frame living
        # inside an internal canvas, while a separate internal
        # `_parent_frame` is what's really pack-managed in `content`.
        # CTk transparently redirects calls made ON file_grid (like
        # file_grid.pack(...)) to the right internal widget, but using
        # file_grid as a `before=`/`after=` reference FROM another
        # widget resolves to its real (non-pack-managed) path and
        # raises "isn't packed". `header` is a plain CTkFrame with no
        # such indirection, so it's a safe anchor to pack relative to.
        progress_bar.pack(fill="x", pady=(0, 10), after=header)
        progress_bar.set(0)
        app.update_idletasks()

    def hide_progress():
        progress_bar.pack_forget()

    def on_progress(fraction):
        progress_bar.set(fraction)
        app.update_idletasks()
        if fraction >= 1.0:
            app.after(400, hide_progress)

    def do_upload():
        show_progress()
        upload_file(progress_callback=on_progress)
        load_files()

    upload.configure(command=do_upload)

    search.bind("<KeyRelease>", lambda e: load_files())

    # =============================
    # Drag & Drop (requires tkinterdnd2)
    # =============================

    if dnd_available and DND_FILES is not None:
        try:
            file_grid.drop_target_register(DND_FILES)

            def on_drop(event):
                paths = app.tk.splitlist(event.data)
                show_progress()
                upload_dropped_files(list(paths), progress_callback=on_progress)
                load_files()

            file_grid.dnd_bind("<<Drop>>", on_drop)
        except Exception:
            pass

    load_files()