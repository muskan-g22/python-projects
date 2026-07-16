import customtkinter as ctk
from tkinter import Menu, simpledialog, messagebox

from utils import get_thumbnail, format_size
from file_manager import open_file, delete_file, rename_file, toggle_favorite, is_favorite
from config import *


def create_card(parent, file, row, column, refresh):

    card = ctk.CTkFrame(
        parent,
        width=CARD_WIDTH,
        height=CARD_HEIGHT,
        corner_radius=CARD_RADIUS,
        fg_color=CARD_BG,
        border_width=1,
        border_color=BORDER
    )

    card.grid(
        row=row,
        column=column,
        padx=GRID_PADDING,
        pady=GRID_PADDING,
        sticky="n"
    )

    card.grid_propagate(False)

    def enter(event):
        card.configure(border_color=PRIMARY, border_width=2)

    def leave(event):
        card.configure(border_color=BORDER, border_width=1)

    card.bind("<Enter>", enter)
    card.bind("<Leave>", leave)

    # -------------------------
    # Favorite Star (top-left corner)
    # -------------------------

    def refresh_star():
        star_btn.configure(
            text="★" if is_favorite(file) else "☆",
            text_color=FAVORITE if is_favorite(file) else TEXT_LIGHT
        )

    def toggle_fav():
        toggle_favorite(file)
        refresh()

    star_btn = ctk.CTkButton(
        card,
        text="★" if is_favorite(file) else "☆",
        width=28,
        height=28,
        corner_radius=14,
        fg_color="transparent",
        hover_color=HOVER,
        text_color=FAVORITE if is_favorite(file) else TEXT_LIGHT,
        font=("Segoe UI", 16),
        command=toggle_fav
    )

    star_btn.place(x=6, y=6)

    # -------------------------
    # Icon / Thumbnail
    # -------------------------

    icon = ctk.CTkLabel(
        card,
        text="",
        image=get_thumbnail(file, THUMB_SIZE)
    )

    icon.pack(pady=(30, 18))

    # -------------------------
    # File Name
    # -------------------------

    filename = file.name

    if len(filename) > 22:
        filename = filename[:19] + "..."

    name = ctk.CTkLabel(
        card,
        text=filename,
        font=CARD_TITLE_FONT,
        text_color=TEXT
    )

    name.pack()

    # -------------------------
    # File Size
    # -------------------------

    size = ctk.CTkLabel(
        card,
        text=format_size(file.stat().st_size),
        font=CARD_SIZE_FONT,
        text_color=TEXT_LIGHT
    )

    size.pack(pady=(8, 35))

    # -------------------------
    # Bottom Area
    # -------------------------

    bottom = ctk.CTkFrame(
        card,
        fg_color="transparent"
    )

    bottom.pack(
        side="bottom",
        fill="x",
        padx=15,
        pady=12
    )

    open_btn = ctk.CTkButton(
        bottom,
        text="↗ Open",
        width=70,
        height=32,
        corner_radius=16,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        font=BUTTON_FONT,
        command=lambda: open_file(file)
    )

    open_btn.pack(side="left")

    # -------------------------
    # Rename
    # -------------------------

    def rename():

        new_name = simpledialog.askstring(
            "Rename File",
            "Enter a new filename:",
            initialvalue=file.name
        )

        if new_name:
            rename_file(file, new_name)
            refresh()

    # -------------------------
    # Delete
    # -------------------------

    def delete():

        answer = messagebox.askyesno(
            "Delete",
            f"Delete '{file.name}'?"
        )

        if answer:
            delete_file(file)
            refresh()

    # -------------------------
    # Context menu (shared by "⋮" button AND right-click)
    # -------------------------

    def show_menu(x, y):

        menu = Menu(tearoff=0)

        menu.add_command(label="↗ Open", command=lambda: open_file(file))
        menu.add_command(
            label="Remove from Favorites" if is_favorite(file) else "Add to Favorites",
            command=toggle_fav
        )
        menu.add_separator()
        menu.add_command(label="Rename", command=rename)
        menu.add_command(label="Delete", command=delete)

        menu.tk_popup(x, y)

    more = ctk.CTkButton(
        bottom,
        text="⋮",
        width=32,
        height=32,
        corner_radius=16,
        fg_color="transparent",
        hover_color=HOVER,
        text_color=TEXT,
        command=lambda: show_menu(more.winfo_rootx(), more.winfo_rooty() + 30)
    )

    more.pack(side="right")

    # -------------------------
    # Double-click to open, right-click for context menu
    # (bound on the whole card AND every child widget so the
    # icon/name/size area is clickable too, not just empty space)
    # -------------------------

    def bind_interactions(widget):
        widget.bind("<Double-Button-1>", lambda e: open_file(file))
        widget.bind("<Button-3>", lambda e: show_menu(e.x_root, e.y_root))

    bind_interactions(card)

    for widget in card.winfo_children():
        # Skip re-binding right-click on the star/menu buttons
        # themselves so their own commands still take priority.
        if widget in (star_btn, more):
            widget.bind("<Double-Button-1>", lambda e: open_file(file))
            continue
        bind_interactions(widget)