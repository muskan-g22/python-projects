from pathlib import Path
from tkinter import filedialog, messagebox
import shutil
import os
import sys
import json
import subprocess

# ============================================
# Storage Folder
# ============================================

storage_folder = Path("storage")
storage_folder.mkdir(exist_ok=True)

# Small app-data folder for favorites/recent tracking
data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

FAVORITES_FILE = data_folder / "favorites.json"
RECENT_FILE = data_folder / "recent.json"

RECENT_LIMIT = 15


# ============================================
# Small JSON helpers (favorites / recent lists)
# ============================================

def _load_json(path):
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def _save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass


# ============================================
# Get Files
# ============================================

def get_files():
    """
    Returns every file inside the storage folder.
    """
    return sorted(
        [file for file in storage_folder.iterdir() if file.is_file()],
        key=lambda file: file.name.lower()
    )


def get_files_by_category(category, extensions_map):
    """
    Filters files by sidebar category ("Dashboard" = everything,
    "Others" = anything not matched by a known category).
    """
    files = get_files()

    if category == "Dashboard":
        return files

    if category == "Others":
        known = set()
        for exts in extensions_map.values():
            known |= exts
        return [f for f in files if f.suffix.lower() not in known]

    exts = extensions_map.get(category, set())
    return [f for f in files if f.suffix.lower() in exts]


# ============================================
# Favorites
# ============================================

def get_favorite_names():
    return set(_load_json(FAVORITES_FILE))


def is_favorite(file):
    return file.name in get_favorite_names()


def toggle_favorite(file):
    favs = get_favorite_names()

    if file.name in favs:
        favs.discard(file.name)
    else:
        favs.add(file.name)

    _save_json(FAVORITES_FILE, list(favs))


def get_favorite_files():
    favs = get_favorite_names()
    return [f for f in get_files() if f.name in favs]


# ============================================
# Recent Files
# ============================================

def add_recent(file):
    recent = _load_json(RECENT_FILE)
    recent = [name for name in recent if name != file.name]
    recent.insert(0, file.name)
    recent = recent[:RECENT_LIMIT]
    _save_json(RECENT_FILE, recent)


def get_recent_files():
    recent_names = _load_json(RECENT_FILE)
    files_by_name = {f.name: f for f in get_files()}
    return [files_by_name[name] for name in recent_names if name in files_by_name]


# ============================================
# Storage Usage
# ============================================

def get_storage_usage():
    return sum(f.stat().st_size for f in get_files())


# ============================================
# Upload (with progress reporting)
# ============================================

def _copy_with_progress(source, destination, progress_callback, file_index, total_files):
    size = source.stat().st_size
    copied = 0
    chunk_size = 1024 * 1024  # 1 MB

    with open(source, "rb") as src, open(destination, "wb") as dst:
        while True:
            chunk = src.read(chunk_size)

            if not chunk:
                break

            dst.write(chunk)
            copied += len(chunk)

            if progress_callback and size > 0:
                file_fraction = copied / size
                overall = (file_index + file_fraction) / total_files
                progress_callback(overall)

    try:
        shutil.copystat(source, destination)
    except Exception:
        pass  # metadata copy failing shouldn't fail the whole upload


def _copy_many(paths, progress_callback=None):
    uploaded = []
    valid_paths = [Path(p) for p in paths if Path(p).is_file()]
    total = len(valid_paths)

    if total == 0:
        return uploaded

    for index, source in enumerate(valid_paths):
        destination = storage_folder / source.name

        if destination.exists():
            messagebox.showwarning("File Exists", f'"{source.name}" already exists.')
            continue

        try:
            _copy_with_progress(source, destination, progress_callback, index, total)
            uploaded.append(destination)
        except Exception as e:
            messagebox.showerror("Upload Error", str(e))

    if progress_callback:
        progress_callback(1.0)

    return uploaded


def upload_file(progress_callback=None):
    """
    Opens a file picker (supports multi-select) and copies
    the chosen files into storage, reporting progress via
    progress_callback(fraction: float).
    """
    filenames = filedialog.askopenfilenames(title="Choose file(s)")

    if not filenames:
        return []

    return _copy_many(filenames, progress_callback)


def upload_dropped_files(paths, progress_callback=None):
    """
    Same as upload_file, but for paths coming from an
    OS drag-and-drop event instead of a file dialog.
    """
    return _copy_many(paths, progress_callback)


# ============================================
# Delete
# ============================================

def delete_file(file):
    try:
        file.unlink()

        favs = get_favorite_names()
        if file.name in favs:
            favs.discard(file.name)
            _save_json(FAVORITES_FILE, list(favs))

        recent = _load_json(RECENT_FILE)
        if file.name in recent:
            recent.remove(file.name)
            _save_json(RECENT_FILE, recent)

    except Exception as e:
        messagebox.showerror("Delete Error", str(e))


# ============================================
# Rename
# ============================================

def rename_file(file, new_name):

    new_name = new_name.strip()

    if not new_name:
        return

    new_path = file.parent / new_name

    if new_path.exists():
        messagebox.showwarning("Rename", "A file with this name already exists.")
        return

    try:
        old_name = file.name
        file.rename(new_path)

        favs = get_favorite_names()
        if old_name in favs:
            favs.discard(old_name)
            favs.add(new_name)
            _save_json(FAVORITES_FILE, list(favs))

        recent = _load_json(RECENT_FILE)
        recent = [new_name if n == old_name else n for n in recent]
        _save_json(RECENT_FILE, recent)

    except Exception as e:
        messagebox.showerror("Rename Error", str(e))


# ============================================
# Open (now cross-platform: Windows / macOS / Linux)
# ============================================

def open_file(file):
    try:
        add_recent(file)

        if sys.platform == "win32":
            os.startfile(file)  # noqa: (Windows-only API, guarded above)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(file)])
        else:
            subprocess.Popen(["xdg-open", str(file)])

    except Exception as e:
        messagebox.showerror("Open Error", str(e))