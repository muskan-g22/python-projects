# 📂 File Organizer

A desktop file organizer built with Python and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — browse, upload, and manage your files through a clean, card-based interface with favorites, recent files, dark mode, drag & drop, and more.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 🗂️ **Category browsing** — files auto-sorted into Documents, Images, Videos, Audio, and Others
- 🖱️ **Drag & Drop** — drop files straight from your file explorer into the app
- 📋 **Right-click context menu** — Open, Favorite, Rename, Delete
- ⭐ **Favorites** — star any file for quick access
- 🕒 **Recent Files** — automatically tracks the last files you opened
- 🌙 **Dark Mode** — toggle between light and dark themes
- 🖼️ **Thumbnail Previews** — real image previews for photos, icons for everything else
- 📊 **Upload Progress Bar** — live progress while files are copied in
- 💾 **Storage Usage** — see how much space your files are using at a glance
- 🔍 **Search** — instantly filter files by name

## 🖥️ Screenshots
![alt text](image-3.png)
![alt text](image-4.png)
## 🛠️ Tech Stack

- **Python 3.10+**
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** — modern-looking Tkinter widgets
- **[Pillow](https://python-pillow.org/)** — image handling and thumbnail generation
- **[tkinterdnd2](https://github.com/pmgagne/tkinterdnd2)** — native OS drag & drop support (optional)

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/muskan-g22/python-projects/tree/main/File-organizer
   cd file-organizer
   ```

2. **(Recommended) Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
    pip install customtkinter
    pip install Pillow
    pip install tkinterdnd2
   ```

## ▶️ Usage

Run the app from the project folder:

```bash
python main.py
```

On first launch, the app creates two local folders next to `main.py`:

- `storage/` — where all your organized files actually live
- `data/` — small JSON files tracking favorites and recent files (not your actual documents)

Use the **+ Upload** button (or drag files onto the window) to add files, then browse, search, favorite, rename, or delete them from the sidebar and file cards.

> **Note:** Drag & drop requires `tkinterdnd2`. If it isn't installed, the app still runs fine — you'll just see a small tip in the UI and can use the Upload button instead.

## 📁 Project Structure

```
file-organizer/
├── main.py           # App entry point
├── ui.py              # Main window layout, sidebar, top bar, file grid
├── cards.py           # Individual file card widget (icon, name, menu, favorite star)
├── file_manager.py    # File operations: upload, delete, rename, favorites, recent, storage usage
├── utils.py           # Icon loading, thumbnail generation, file size formatting
├── config.py          # Colors, fonts, sizes, and category definitions
└── README.md
```

## 🗺️ Roadmap / Ideas

- [ ] File tagging / custom folders
- [ ] Bulk select and batch actions (delete/move multiple files)
- [ ] Cloud storage sync (Google Drive / Dropbox)
- [ ] File preview panel (open PDFs/text without leaving the app)

## 🤝 Contributing

This is a personal project, but suggestions and pull requests are welcome — feel free to open an issue if you spot a bug or have an idea.

## 📄 License

This project is licensed under the MIT License — feel free to use and modify it for your own projects.