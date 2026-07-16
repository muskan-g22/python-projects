from pathlib import Path
from PIL import Image
import customtkinter as ctk

ICON_CACHE = {}
THUMB_CACHE = {}

ICON_DIR = Path("assets/icons")

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}

_ICON_MAP = {
    ".pdf": "pdf.png",
    ".doc": "document.png",
    ".docx": "document.png",
    ".txt": "document.png",
    ".xls": "document.png",
    ".xlsx": "document.png",
    ".ppt": "document.png",
    ".pptx": "document.png",
    ".jpg": "image.png",
    ".jpeg": "image.png",
    ".png": "image.png",
    ".gif": "image.png",
    ".bmp": "image.png",
    ".webp": "image.png",
    ".mp4": "video.png",
    ".avi": "video.png",
    ".mkv": "video.png",
    ".mov": "video.png",
    ".mp3": "audio.png",
    ".wav": "audio.png",
    ".flac": "audio.png",
    ".zip": "zip.png",
    ".rar": "zip.png",
}

_FALLBACK_ICON = "file.png"


def _blank_image(size):
    """Used if an icon file is missing, so the app never crashes."""
    return Image.new("RGBA", size, (0, 0, 0, 0))


def _load_ctk_image(path, size):
    key = (str(path), size)

    if key in ICON_CACHE:
        return ICON_CACHE[key]

    try:
        image = Image.open(path)
        image = image.convert("RGBA")
    except Exception:
        # Icon file missing/corrupt -> fall back to a blank
        # transparent image instead of crashing the whole app.
        image = _blank_image(size)

    ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=size)
    ICON_CACHE[key] = ctk_image
    return ctk_image


def get_icon(extension, size=(64, 64)):
    extension = extension.lower()
    filename = _ICON_MAP.get(extension, _FALLBACK_ICON)
    path = ICON_DIR / filename

    if not path.exists():
        path = ICON_DIR / _FALLBACK_ICON

    return _load_ctk_image(path, size)


def get_thumbnail(file, size=(64, 64)):
    """
    Returns a real preview thumbnail for image files.
    Falls back to the generic type icon for everything else
    (or if the image can't be opened/decoded).
    """
    extension = file.suffix.lower()

    if extension not in IMAGE_EXTENSIONS:
        return get_icon(extension, size)

    try:
        mtime = file.stat().st_mtime
    except Exception:
        mtime = 0

    cache_key = (str(file), mtime, size)

    if cache_key in THUMB_CACHE:
        return THUMB_CACHE[cache_key]

    try:
        image = Image.open(file)
        image = image.convert("RGBA")
        image.thumbnail(size)
    except Exception:
        return get_icon(extension, size)

    ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=image.size)
    THUMB_CACHE[cache_key] = ctk_image
    return ctk_image


def format_size(size):

    if size < 1024:
        return f"{size} B"

    elif size < 1024**2:
        return f"{size/1024:.1f} KB"

    elif size < 1024**3:
        return f"{size/(1024**2):.1f} MB"

    return f"{size/(1024**3):.1f} GB"