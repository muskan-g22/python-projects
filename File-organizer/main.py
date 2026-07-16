import customtkinter as ctk
from ui import build_ui

# tkinterdnd2 gives us real OS-level drag & drop (dragging a file
# from Explorer/Finder/File Manager straight into the app window).
# It's optional: if it isn't installed, the app still runs fine,
# just without drag & drop (the Upload button still works).
#
# Note: importing tkinterdnd2.TkinterDnD adds drop_target_register()/
# dnd_bind() to every tkinter widget class as a side effect, so we
# don't need (and shouldn't use) a TkinterDnD.Tk/ctk.CTk multiple-
# inheritance subclass - that combination breaks CustomTkinter's
# internal window-scaling setup. We just need to load the tkdnd Tcl
# package into our existing CTk root via TkinterDnD._require().
try:
    from tkinterdnd2 import TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

if DND_AVAILABLE:
    try:
        TkinterDnD._require(app)
    except Exception:
        DND_AVAILABLE = False

build_ui(app, dnd_available=DND_AVAILABLE)

app.mainloop()