# ==============================
# WINDOW
# ==============================

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 850

APP_TITLE = "File Organizer"


# ==============================
# COLORS
# Each color is a (light_mode, dark_mode) tuple.
# CustomTkinter automatically swaps between them
# when ctk.set_appearance_mode() is called, so
# dark mode "just works" for every widget below
# without needing to manually re-theme anything.
# ==============================

APP_BG = ("#F6F7FB", "#1A1B26")
SIDEBAR_BG = ("#FFFFFF", "#20212E")
TOPBAR_BG = ("#FFFFFF", "#20212E")
CONTENT_BG = ("#F6F7FB", "#1A1B26")
CARD_BG = ("#FFFFFF", "#262837")
BORDER = ("#E9ECF2", "#333548")

PRIMARY = ("#5B6CFF", "#7C8CFF")
PRIMARY_HOVER = ("#4A59F5", "#6B7BFF")

TEXT = ("#1F2937", "#E5E7EB")
TEXT_LIGHT = ("#6B7280", "#9399A8")

HOVER = ("#EEF2FF", "#2E3040")

DANGER = ("#EF4444", "#F87171")
DANGER_HOVER = ("#DC2626", "#EF4444")

FAVORITE = ("#F5A524", "#FBBF24")


# ==============================
# SIDEBAR
# ==============================

SIDEBAR_WIDTH = 250
MENU_HEIGHT = 42
MENU_RADIUS = 12


# ==============================
# TOP BAR
# ==============================

TOPBAR_HEIGHT = 75
SEARCH_WIDTH = 380
SEARCH_HEIGHT = 42
UPLOAD_HEIGHT = 42


# ==============================
# FILE CARDS
# ==============================

CARD_WIDTH = 240
CARD_HEIGHT = 250
CARD_RADIUS = 20
CARD_PADDING = 20
GRID_PADDING = 20
CARDS_PER_ROW = 4          # fallback if width can't be measured yet
THUMB_SIZE = (64, 64)


# ==============================
# FONTS
# ==============================

TITLE_FONT = ("Segoe UI", 30, "bold")
SUBTITLE_FONT = ("Segoe UI", 16)
CARD_TITLE_FONT = ("Segoe UI", 15, "bold")
CARD_SIZE_FONT = ("Segoe UI", 12)
MENU_FONT = ("Segoe UI", 15)
BUTTON_FONT = ("Segoe UI", 13)


# ==============================
# CATEGORIES
# Maps sidebar category names to the file
# extensions that belong in them.
# ==============================

CATEGORY_EXTENSIONS = {
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"},
    "Videos": {".mp4", ".avi", ".mkv", ".mov", ".wmv"},
    "Audio": {".mp3", ".wav", ".flac", ".aac"},
}

RECENT_LIMIT = 15

# Used only to render the storage usage bar in the sidebar.
STORAGE_LIMIT_GB = 10